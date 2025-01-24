#!/bin/bash

COL_NAME=$1

echo "Collection: $COL_NAME"

if [[ -z "$1"] ]]; then
	echo "You should pass the name of the collection as a parameter"
	exit 1
fi

create_table=$(cat << EOF
create table $COL_NAME (
	id serial,
	category text,
	metadata jsonb,
	body text,
	embedding vector(8192),
	update_at timestamp default now(),
	primary key (id)
);
EOF
)
# TODO: create indexes for the columns category, metadata and body

# creating the table for the collection $COL_NAME
sudo -u postgres psql -d rag -c "$create_table"

if [[ "$?" -eq "0" ]]; then
	echo "Collection $COL_NAME was created"
else
	echo "Error creating collection"
fi

