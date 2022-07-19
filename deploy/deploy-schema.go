package main

import (
	"encoding/xml"
	"fmt"
	"github.com/antchfx/xmlquery"
	"github.com/antchfx/xpath"
	"github.com/beevik/etree"
	flag "github.com/ogier/pflag"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
)

// flags
var (
	sour string
	dest string
)

func main() {
	flag.Parse()
	if flag.NFlag() == 0 {
		fmt.Printf("Usage: %s [options]\n", os.Args[0])
		fmt.Println("Options:")
		flag.PrintDefaults()
		os.Exit(1)
	}
	_, _ = runEtree(dest, sour)
}

func init() {
	flag.StringVarP(&sour, "source", "s", "", "Path to schema: ")
	flag.StringVarP(&dest, "destination", "d", "", "Path to deploy the schema: ")
}

func runEtree(deployed, searchDir string) ([]string, error) {
	fileList := make([]string, 0)
	e := filepath.Walk(searchDir, func(path string, f os.FileInfo, err error) error {
		if strings.HasSuffix(path, ".xsd") {
			fileList = append(fileList, path)
			b, err := ioutil.ReadFile(path)
			if err != nil {
				fmt.Print(err)
			}
			str := string(b)
			// start XSD sorting by @name
			docin, err := xmlquery.Parse(strings.NewReader(str))
			list := xmlquery.Find(docin, "/xsd:schema/*[@name]")
			expr, err := xpath.Compile("count(/xsd:schema/*[@name])")
			var amount = expr.Evaluate(xmlquery.CreateXPathNavigator(docin)).(float64)
			var elementNames = make([]string, int(amount))
			for _, k := range list {
				elementNames = append(elementNames, k.SelectAttr("name"))
			}
			sort.Strings(elementNames)
			// new output XSD document
			doc := &xmlquery.Node{
				Type: xmlquery.DeclarationNode,
				Data: "xml",
				Prefix: "xsd",
				Attr: []xml.Attr{
					{Name: xml.Name{Local: "version"}, Value: "1.0"},
					{Name: xml.Name{Local: "encoding"}, Value: "UTF-8"},
				},
			}
			x := xmlquery.FindOne(docin, "/*")
			root := &xmlquery.Node{
				Data: "schema",
				Prefix: "xsd",
				Type: xmlquery.DocumentNode,
				Attr: x.Attr,
			}
			doc.FirstChild = root
			var r []string
			for _, str := range elementNames {
				if str != "" {
					r = append(r, str)
				}
			}
			current := root
			imps := xmlquery.Find(docin, "//xsd:import")
			if imps != nil {
				expr, _ := xpath.Compile("count(//xsd:import)")
				amount := expr.Evaluate(xmlquery.CreateXPathNavigator(docin)).(float64)
				var schemaImports = make([]string, int(amount))
				for _, k := range imps {
					schemaImports = append(schemaImports, k.SelectAttr("namespace"))
				}
				sort.Strings(schemaImports)
				var filteredImports []string
				for _, str := range schemaImports {
					if str != "" {
						filteredImports = append(filteredImports, str)
					}
				}
				for i, k := range filteredImports {
					x := xmlquery.FindOne(docin, "//xsd:import[@namespace='"+k+"']")
					if i == 0 {
						root.FirstChild = &xmlquery.Node{
							Data: x.Data,
							Prefix: "xsd",
							Type: xmlquery.ElementNode,
							Attr: x.Attr,}
						current = root.FirstChild
					} else {
						element := &xmlquery.Node{
							Prefix: "xsd",
							Data: x.Data,
							Type: xmlquery.ElementNode,
							Attr: x.Attr,}
						current.NextSibling = element
						current = current.NextSibling
					}
				}
			}
			for _, k := range r {
				x := xmlquery.FindOne(docin, "/*/*[@name='"+k+"']")
				element := &xmlquery.Node{
					Prefix: "xsd",
					Data: x.Data,
					Type: xmlquery.ElementNode,
					Attr: x.Attr,}
				if current == root {
					root.FirstChild = element
					current = root.FirstChild
				} else {
					current.NextSibling = element
					current = current.NextSibling
				}
				children := xmlquery.FindOne(docin, "/*/*[@name='"+k+"']/*")
				current.FirstChild = children
			}
			output := doc.OutputXML(true)

			// hack it for now - not needed now
			/*
			re := regexp.MustCompile("(?m)(</?)([a-z]{2,}.*?>)")
			output = re.ReplaceAllString(output,"${1}xsd:${2}")

			re = regexp.MustCompile("(?m)(</?)(xsd)(:displayterm.*?>)")
			output = re.ReplaceAllString(output,"${1}dtyp${3}")

			// replace version
			re := regexp.MustCompile("(?s)(.*<xsd:schema.*version=\")(.*?)(\".*?>.*</xsd:schema>.*)")  // flag 's' for . to match newline
			output = re.ReplaceAllString(output,"${1}"+version+"${3}")
			*/
			
			// replace t24ref links
			re := regexp.MustCompile(`(?i)(\[d:t24ref/\]) ?(([a-z]*\d+(-\d+)*(\.\d+)*)(\(([a-z]\)([\da-z]( &amp; \d+)*)*(\([a-z]*\))*))*)`)
			output = re.ReplaceAllString(output, "[d:t24ref h=\"${2}\"/]")

			// replace [ t24ref ] to < t4ref >
			re = regexp.MustCompile(`(\[)(/?d:.+?/?)(\])`)
			output = re.ReplaceAllString(output,"<${2}>")

			var htmlEscaper = strings.NewReplacer( `&`, "&amp;",)
			output = htmlEscaper.Replace(output)


			re = regexp.MustCompile("&amp;#34;")
			output = re.ReplaceAllString(output, "\"")

			re = regexp.MustCompile("&amp;#xA;")
			output = re.ReplaceAllString(output, "\n")

			re = regexp.MustCompile("&amp;#39;")
			output = re.ReplaceAllString(output, "'")

			//fmt.Println(output)
			//os.Exit(1)

			doc1 := etree.NewDocument()
			if err := doc1.ReadFromString(output); err != nil {
				panic(err)
			}
			doc1.Root().SortAttrs()
			doc1.Indent(3)
			outputDoc, _ := doc1.WriteToString()

			re = regexp.MustCompile("&quot;")
			outputDoc = re.ReplaceAllString(outputDoc, "\"")

			re = regexp.MustCompile("&amp;#xA;")
			outputDoc = re.ReplaceAllString(outputDoc, "\n")

			re = regexp.MustCompile("&apos;")
			outputDoc = re.ReplaceAllString(outputDoc, "'")

			// whitespace between 'ft' and '2' etc
			re = regexp.MustCompile(` *\r?\n *<d:su`)
			outputDoc = re.ReplaceAllString(outputDoc, "<d:su")

			outputPath := strings.Split(path, string(os.PathSeparator))
			outputDir := outputPath[len(outputPath)-2]
			outputFile := outputPath[len(outputPath)-1]

			_ = os.MkdirAll(filepath.Join(deployed, outputDir), os.ModePerm)
			err = ioutil.WriteFile(filepath.Join(deployed, outputDir, outputFile), []byte(outputDoc), 0755)
			if err != nil {
				fmt.Print(err)
			}
		}
		return err
	})
	if e != nil {
		panic(e)
	}
	for _, file := range fileList {
		fmt.Println("Processed: ", file)
	}
	return fileList, nil
}
