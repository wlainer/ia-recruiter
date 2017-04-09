package com.vanhackathon;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.Parser;
import org.apache.tika.sax.BodyContentHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.xml.sax.SAXException;

import opennlp.tools.namefind.NameFinderME;
import opennlp.tools.namefind.TokenNameFinderModel;
import opennlp.tools.tokenize.SimpleTokenizer;
import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.util.Span;

public class BasicNameFinder {

	public static void main(String[] args) throws IOException, SAXException, TikaException {

		Logger log = LoggerFactory.getLogger(BasicNameFinder.class);

		BasicNameFinder toi = new BasicNameFinder();
		String cnt = toi.contentEx();
		System.out.println("");

		// Load the model file downloaded from OpenNLP
		// http://opennlp.sourceforge.net/models-1.5/en-ner-person.bin
		// TokenNameFinderModel model = new TokenNameFinderModel(new File(
		// "input/en-ner-person.bin"));

		TokenNameFinderModel model = new TokenNameFinderModel(new File("input/en-ner-skills.bin"));

		// Create a NameFinder using the model
		NameFinderME finder = new NameFinderME(model);

		Tokenizer tokenizer = SimpleTokenizer.INSTANCE;

		// Split the sentence into tokens
		String[] tokens = tokenizer.tokenize(cnt);

		// Find the names in the tokens and return Span objects
		Span[] nameSpans = finder.find(tokens);

		// Print the names extracted from the tokens using the Span data
		log.info(Arrays.toString(Span.spansToStrings(nameSpans, tokens)));

	}

	public String contentEx() throws IOException, SAXException, TikaException {
		InputStream is = new BufferedInputStream(new FileInputStream(new File("examples/job.pdf")));
		Parser ps = new AutoDetectParser(); // for detect parser related to

		BodyContentHandler bch = new BodyContentHandler();

		ps.parse(is, bch, new Metadata(), new ParseContext());

		return bch.toString();

	}
}