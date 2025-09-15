# This program is intended to turn the PDF links from LOC API call's PDF results into OCR-ed plain text. This process involves turning XML files into plain TXT.

import os, csv, requests, re, gc, io
import pandas as pd
import xml.etree.ElementTree as ET

class ExtractCSV:
    def __init__(self, CSVFilePath: str):
        self.CSVFilePath = CSVFilePath
        self.csvDataFrame = pd.read_csv(CSVFilePath)

    # -------------------------------
    # Helpers
    # -------------------------------
    def makeFileName(self, partOfFileName):
        """Make string safe for filenames (remove spaces and bad chars)."""
        return re.sub(r'[^A-Za-z0-9_-]+', '', partOfFileName.replace(" ", "_"))

    def xmlToPlainText(self, xmlContent):
        """Convert ALTO XML content into plain text with newlines preserved (namespace-agnostic)."""
        # Remove namespaces by reparsing
        it = ET.iterparse(io.BytesIO(xmlContent))
        for _, el in it:
            if "}" in el.tag:
                el.tag = el.tag.split("}", 1)[1]  # strip namespace
        root = it.root

        all_lines = []
        for textblock in root.findall(".//TextBlock"):
            block_lines = []
            for textline in textblock.findall("TextLine"):
                words = [
                    string.attrib.get("CONTENT", "")
                    for string in textline.findall("String")
                ]
                if words:
                    block_lines.append(" ".join(words))
            if block_lines:
                all_lines.append("\n".join(block_lines))

        return "\n\n".join(all_lines)

    # -------------------------------
    # Core methods
    # -------------------------------
    def turnColumnIntoList(self, column="PDF Link"):
        """Convert a column into a Python list."""
        return self.csvDataFrame[column].tolist()

    def turnPDFLinkIntoXMLLink(self):
        """Return list of (PDFLink, XMLLink)."""
        pdf_links = self.turnColumnIntoList("PDF Link")
        return [(link, link[:-3] + "xml") for link in pdf_links]

    def downloadAndProcessXML(self, txtDirectory="txt_out", xmlDirectory="xml_out", failedFile="failed_links.txt"):
        """Download XML, save raw XML and parsed TXT with descriptive names. 
        Log any failed/empty results into a separate file."""
        os.makedirs(txtDirectory, exist_ok=True)
        os.makedirs(xmlDirectory, exist_ok=True)

        failedLinks = []

        for i, row in self.csvDataFrame.iterrows():
            try:
                # Build filename base from metadata
                filename_base = "_".join([
                    self.makeFileName(str(row["NewspaperTitle"])),
                    self.makeFileName(str(row["IssueDate"])),
                    self.makeFileName(str(row["City"])),
                    self.makeFileName(str(row["State"])),
                    self.makeFileName(str(row["Region"])),
                    f"p{row['PageNumber']}",
                ])

                xmlURLLink = row["PDF Link"][:-3] + "xml"

                # Download XML
                response = requests.get(xmlURLLink, stream=True)
                response.raise_for_status()
                xmlContent = response.content

                # Save raw XML
                xmlPath = os.path.join(xmlDirectory, filename_base + ".xml")
                with open(xmlPath, "wb") as f:
                    f.write(xmlContent)

                # Parse XML into TXT
                text = self.xmlToPlainText(xmlContent)
                txtPath = os.path.join(txtDirectory, filename_base + ".txt")
                with open(txtPath, "w", encoding="utf-8") as f:
                    f.write(text)

                if not text.strip():
                    failedLinks.append(xmlURLLink)
                    print(f"[{i+1}/{len(self.csvDataFrame)}] EMPTY TEXT for {xmlURLLink}")
                else:
                    print(f"[{i+1}/{len(self.csvDataFrame)}] Saved {txtPath} and {xmlPath}")

            except Exception as e:
                print(f"Error with row {i} ({row['PDF Link']}): {e}")
                failedLinks.append(row["PDF Link"])

            finally:
                # Free memory after each file
                del response, xmlContent
                gc.collect()

        # Save failed links to file
        if failedLinks:
            with open(failedFile, "w", encoding="utf-8") as f:
                for link in failedLinks:
                    f.write(link + "\n")
            print(f"\nSaved {len(failedLinks)} failed links to {failedFile}")
        else:
            print("\nAll files processed with non-empty text.")


    # -------------------------------
    # Auxiliary
    # -------------------------------
    def checkBlankCells(self, column="Region"):
        """Check how many blank cells are in a given column."""
        blankCounter = 0
        with open(self.CSVFilePath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            if column not in reader.fieldnames:
                raise ValueError(f"CSV does not contain a '{column}' column.")

            for row in reader:
                if row[column] is None or row[column].strip() == "":
                    blankCounter += 1

        return blankCounter

if __name__ == "__main__":
    CSVFilePath = "/Users/Jerry/Desktop/DHproj-reading/LAOilProject/LAOil/DataFolder/testCSVNewspaperWithXMLLinks.csv"
    extractor = ExtractCSV(CSVFilePath)

    # Choose your own folders
    txtFolder = "/Volumes/JZ/LAOilTXTXML/TXTOutput"
    xmlFolder = "/Volumes/JZ/LAOilTXTXML/XMLOutput"

    extractor.downloadAndProcessXML(txtDirectory=txtFolder, xmlDirectory=xmlFolder)