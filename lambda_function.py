from numpy import ndarray, where
from constants.qr_module_characters import MODULE
from main import generate_qr_code

def convert_to_list(matrix: ndarray) -> list:
    matrix = where(matrix == MODULE['white'], 0, 1)
    return matrix.tolist()

def lambda_handler(event, context):
    try:
        data = event.get('data', 'https://dhruvanarayan.com')
        error_correction_level = event.get('error_correction', 'L')
        if error_correction_level not in ['L', 'M', 'Q', 'H']:
            raise ValueError("Invalid error correction level. Choose from 'L', 'M', 'Q', 'H'.")
        qr_code = generate_qr_code(data, error_correction_level)
        return {
            'statusCode': 200,
            "headers": { "Content-Type": "application/json" },
            'body': convert_to_list(qr_code)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            "headers": { "Content-Type": "application/json" },
            'body': str(e)
        }