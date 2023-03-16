-- enable pg_vector
CREATE EXTENSION IF NOT EXISTS vector;

-- documents table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    written_year INTEGER,
    document_type TEXT NOT NULL
    );

-- sentences table
CREATE TABLE sentences (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,
    position INTEGER NOT NULL
    );


