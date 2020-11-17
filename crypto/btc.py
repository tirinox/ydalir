import io

import qrcode
from bit import PrivateKey


def make_keys():
    key = PrivateKey()
    code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )
    code.add_data(f'bitcoin:{key.address}')
    code.make(fit=True)
    img = code.make_image(fill_color="black", back_color="white")
    with io.BytesIO() as output:
        img.save(output, format="PNG")
        contents = output.getvalue()
        return contents, key