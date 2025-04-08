import yaml

def default_settings():
    settings = {
        'game': {
            'title': 'Default settings',
            'fps': 60,
            'stallness_factor': 100,
            'screen_width': 800,
            'screen_height': 600,
            'bluebox_width': 50,
            'bluebox_height': 50,
            'redbox_width': 70,
            'redbox_height': 70
        },
        'model': {
            'input_size': 4,
            'hidden_size': 64,
            'output_size': 2,
            'num_moves': 5
        },
        'training': {
            'num_epochs': 200,
            'batch_size': 32,
            'learning_rate': 0.001,
            'shuffle': True,
            'drop_columns': ['Execution', 'clock'],
            'input_columns': ['current_position_x', 'current_position_y', 'target_position_x', 'target_position_y'],
            'output_columns': ['move_x', 'move_y'],
        }
    }
    return settings

def parse_yaml(file_path):
  import yaml
  with open(file_path, 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)
      return default_settings()