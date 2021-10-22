CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

/*
- uuid (universally unique identifier) Este identificador se utiliza de forma perfecta para poder
guardar datos que vayan a variar en ningun momento mientras exista la instacia de la tabla.
- Los Tweets requirieron suministrarle unos VARCHAR de 500 caracteres, aun teniendo en cuenta que
limite de caracteres de Twitter es de 280 cuando fueron evaluados los caracteres para almacenarlos
sobrepasaba el limite por aquellos caracteres que el formato no podía codificar, debido a esto ellos
pusimos casi el doble para tener holgura al momento de ingresar caracteres.
*/

CREATE TABLE IF NOT EXISTS tweets_model (
	tweet_id uuid PRIMARY KEY DEFAULT UUID_GENERATE_V4(), 
	tweet_date VARCHAR (50),
	tweet_username VARCHAR ( 50 ),
	tweet VARCHAR (500),
	tweet_tokenized VARCHAR (1000),
	tweet_translated VARCHAR (500),
	tweet_translated_tokenized VARCHAR (1000),
	tweet_sentiment VARCHAR (50),
	tweet_opinion VARCHAR (50)
);

CREATE TABLE IF NOT EXISTS tweets_test (
	tweet_id uuid PRIMARY KEY DEFAULT UUID_GENERATE_V4(), 
	tweet_date VARCHAR (50),
	tweet_username VARCHAR ( 50 ),
	tweet VARCHAR (500),
	tweet_tokenized VARCHAR (1000),
	tweet_translated VARCHAR (500),
	tweet_translated_tokenized VARCHAR (1000),
	tweet_sentiment VARCHAR (50),
	tweet_opinion VARCHAR (50)
);

CREATE TABLE IF NOT EXISTS tweets_model_sentiment (
	tweet_id uuid PRIMARY KEY DEFAULT UUID_GENERATE_V4(), 
	tweet_date VARCHAR (50),
	tweet_username VARCHAR ( 50 ),
	tweet VARCHAR (500),
	tweet_translated VARCHAR (500),
	tweet_sentiment VARCHAR (50),
	tweet_tokenized VARCHAR (1000),
	tweet_translated_tokenized VARCHAR (1000)
);

CREATE TABLE IF NOT EXISTS tweets_model_opinion (
	tweet_id uuid PRIMARY KEY DEFAULT UUID_GENERATE_V4(), 
	tweet_date VARCHAR (50),
	tweet_username VARCHAR ( 50 ),
	tweet VARCHAR (500),
	tweet_translated VARCHAR (500),
	tweet_opinion VARCHAR (50),
	tweet_tokenized VARCHAR (1000),
	tweet_translated_tokenized VARCHAR (1000)
);

CREATE TABLE IF NOT EXISTS stadistics (
	stadistic_id uuid PRIMARY KEY DEFAULT UUID_GENERATE_V4(), 
	stadistic_accuracy float NOT NULL,
	stadistic_precision float NOT NULL, 
	stadistic_recall float NOT NULL,
	stadistic_f1_score float NOT NULL, 
	stadistic_accuary_all float NOT NULL, 
	stadistic_precisio_all float NOT NULL, 
	stadistic_recall_all float NOT NULL,
	stadistic_f1_score_all float NOT NULL
);


INSERT INTO tweets_model (tweet_date, tweet_username,tweet,tweet_translate,tweet_sentiment,tweet_opinion)
VALUES ('10/3/2021','yocsinm','Si no vas a hacer nada por tu pais mejor vete','If you are not going to do anything for your country, you better leave.','ira','en contra');

SELECT * FROM tweets_model
SELECT * FROM tweets_test
SELECT * FROM stadistics