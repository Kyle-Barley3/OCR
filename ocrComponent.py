import argparse

import spacy  # open-source library for NLP (Natural Language Processing)

EMAILEXT = (".com", ".edu", ".net")  # accepted email extensions, also used to obtain email address.


class ContactInfo:
    def __init__(self):  # contact information to be extracted is name, phone number, and email address
        self.fullName = ""
        self.phoneNumber = ""
        self.emailAddress = ""

    # Spacy can process language and label words/phrases as a person.
    # Thus if the line contains the spacy label 'PERSON' we have found the person's name.
    def getName(self, document):
        langProcessor = spacy.load('en_core_web_md')
        for line in document:
            processedText = langProcessor(line)
            for item in processedText.ents:
                if item.label_ == "PERSON":
                    self.fullName = item.text

    # Phone numbers can be extracted by first checking if 'Phone' or 'Tel' is contained in the line.
    # If not, then we know that the phone number shouldn't contain any letters.
    # Thus if the line doesn't contain any letters, we have found the phone number
    def getPhoneNumber(self, document):
        for line in document:
            if line.__contains__("Phone") or line.__contains__("Tel"):
                for char in line:
                    if char.isdigit():
                        self.phoneNumber = self.phoneNumber + char
            else:
                if not any(char.isalpha() for char in line):
                    for char in line:
                        if char.isdigit():
                            self.phoneNumber = self.phoneNumber + char

    # Email addresses consist of an '@' character as well as some kind of email extension.
    # Thus if line contains the '@' character and one of the accepted email extensions
    # then we know we have found the email address.
    def getEmailAddress(self, document):
        for line in document:
            if line.__contains__("@") and any(ext in line for ext in EMAILEXT):
                self.emailAddress = line

    def getContactInfo(self, document):  # call functions to extract contact information
        self.getEmailAddress(document)
        self.getPhoneNumber(document)
        self.getName(document)


def BusinessCardParser():
    parser = argparse.ArgumentParser()  # Parser to parse arguments passed

    parser.add_argument('--file',
                        help='Path to txt file with results of OCR component',
                        type=str,
                        required=True)

    args = parser.parse_args()
    fh = open(args.file, 'r')
    document = fh.read().split('\n')
    fh.close()

    userContactInfo = ContactInfo()
    userContactInfo.getContactInfo(document)
    print ("Name: " + userContactInfo.fullName)
    print ("Phone: " + userContactInfo.phoneNumber)
    print ("Email: " + userContactInfo.emailAddress)


def main():
    BusinessCardParser()


if __name__ == "__main__":
    main()
