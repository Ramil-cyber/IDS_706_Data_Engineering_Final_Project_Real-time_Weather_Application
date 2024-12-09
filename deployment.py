from src import WeatherDatabaseApi
import os 

def ensure_nested_directory_exists(parent_directory, child_directory):
    """
    Ensure a nested directory structure exists. Create the parent and child directories if necessary.

    :param parent_directory: Name of the parent directory.
    :param child_directory: Name of the child directory inside the parent.
    """
    full_path = os.path.join(parent_directory, child_directory)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"Directory structure '{parent_directory}/{child_directory}' created.")
    else:
        print(f"Directory structure '{parent_directory}/{child_directory}' already exists.")

def setup_application_structure():
    """
    Set up the application's directory structure by ensuring
    'data/db' exists.
    """
    parent_directory = 'data'
    child_directory = 'db'
    ensure_nested_directory_exists(parent_directory, child_directory)

if __name__ == "__main__":
    setup_application_structure()
    test_connection = WeatherDatabaseApi( 'data/db/application', deploy_database = True )
