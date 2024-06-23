import sys
import argparse
import main

# Define the available models
available_models = ['tfidf', 'word2vec', 'bert']

parser = argparse.ArgumentParser(description='Process a query using different models')

# Add the query as a positional argument
parser.add_argument('query', type=str, nargs='?', default='', help='Query to process')

# Add the --create_database flag
parser.add_argument('--create_database', action='store_true', help='Create the database')

# Add the --create_models flag
parser.add_argument('--create_models', nargs='+', help='Create the pre-trained models')

# Add the --list_models flag
parser.add_argument('-lm', '--list_models', action='store_true', help='List available models')

# Add the --models flag with -m as a shortcut
parser.add_argument('-m', '--models', nargs='+', default=available_models, help='Models to use')

# Parse the arguments
args = parser.parse_args()

# If --list_models is specified, print the available models and exit
if args.list_models:
    if vars(args) != {'query': args.query, 'create_database': False, 'create_models': available_models, 'list_models': True, 'models': available_models}:  # Check if any other argument was specified
        print('Error: Cannot use --list_models with other arguments')
        sys.exit()
    print('Available models:', ', '.join(available_models))
    sys.exit()

# If --create_database is specified, create the database and exit
if args.create_database:
    main.create_database()

# If --create_models is specified, create the models and exit
if args.create_models:
    models = args.create_models
    main.create_models(models)

# Use the models selected by the user if models and query are specified
if args.models and args.query != '':
    models = args.models
    query = args.query
    print(f'Selected models: {", ".join(models)}')
    print(f'Query: {query}')

    main.query(models, query)
