import os

from datetime import datetime
from datetime import timedelta
from flask import current_app
from restpki_client import RestPkiClient
from restpki_client import StandardSecurityContexts


def get_restpki_client():
    # ==========================================================================
    #                    >>> PASTE YOUR ACCESS TOKEN BELOW <<<
    # ==========================================================================
    restpki_access_token = 'ruqkIgY805uZm9H5SiDbGJY_It3mMNvQkoGOhYD-TZ8XC56Z8ypNHTjd5Glbuw7RRY8zvRaacpV3hMlFrHlrQz6JFK0xV-LC3xdkGrexGcjizP7MLjQ7ZpCs5-pUJYPwLAK_vhU2XV7Dk-DjKpQHx50TB7wvYqp-Lr0jV9iMok8zcOQZZKZiQjKEm_0wp5Na5LCYHe9nnsRtUEB0u9q2vFYU_lGR8OGRJvpyjTpmL0CClHUS_U5kKO1MxtABdncQYP-_MYO-MbRzkA4jjpSXNKES9kanfAndtBq3GZlg5n3WIX2P8I4tToBj_gQv3Ax32JsZN7dUTCaaLI3lK-9sdPzCH7LQ2YuAmE-D2a_wOxW_TYACSYtF3fu2wmZFEd9_G07uRXxgQfeNXoJA6yjFC_D9d0dHU-C4iM64I1ZcyeX5uOQqlrgQ1ci94Bp91FggDVIk6bGe8iid4a2DCqhYidGpgNkVFGy62HU2yncsS7a0t22D8pA42mZNfc7jo8iu-xowWQ'
    #restpki_access_token = current_app["restpki_access_token"]
    #
    # Throw exception if token is not set (this check is here just for the sake
    # of newcomers, you can remove it)
    if ' API ' in restpki_access_token:
        raise Exception(
            'The API access token was not set! Hint: to run this sample you'
            'must generate an API access token on the REST PKI website and'
            'paste it on the file restpki/utils.py'
        )

    restpki_url = 'https://pki.rest/'
    return RestPkiClient(restpki_url, restpki_access_token)


def get_security_context_id():
    """

    This method is called by all pages to determine the security context to
    be used.

    Security contexts dictate which root certification authorities are
    trusted during certificate validation. In your API calls, you can see
    one of the standard security contexts or reference one of your custom
    contexts.

    :return: StandardSecurityContexts

    """
    if current_app.env == 'development':
        # Lacuna Text PKI (for development purposes only!)
        #
        # This security context trusts ICP-Brasil certificates as well as
        # certificates on Lacuna Software's test PKI. Use it to accept the test
        # certificates provided by Lacuna Software.
        #
        # THIS SHOULD NEVER BE USED ON A PRODUCTION ENVIRONMENT!
        return StandardSecurityContexts.LACUNA_TEST
        # Notice for On Premises users: This security context might not exist on
        # your installation, if you encounter an error please contact developer
        # support.

    else:
        # In production, accepting only certificates from ICP-Brasil
        return StandardSecurityContexts.PKI_BRAZIL


def get_expired_page_headers():
    headers = dict()
    now = datetime.utcnow()
    expires = now - timedelta(seconds=3600)

    headers['Expires'] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers['Last-Modified'] = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers['Cache-Control'] = 'private, no-store, max-age=0, no-cache,' \
                               ' must-revalidate, post-check=0, pre-check=0'
    headers['Pragma'] = 'no-cache'
    return headers


def create_app_data():
    if not os.path.exists(current_app.config['APPDATA_FOLDER']):
        os.makedirs(current_app.config['APPDATA_FOLDER'])


def get_pdf_stamp_content():
    # Read the PDF stamp image
    f = open('%s/%s' % (current_app.static_folder, 'PdfStamp.png'), 'rb')
    pdf_stamp = f.read()
    f.close()
    return pdf_stamp


def get_sample_doc_path():
    return '%s/%s' % (current_app.static_folder, 'SampleDocument.pdf')


def get_sample_nfe_path():
    return '%s/%s' % (current_app.static_folder, 'SampleNFe.xml')


def get_sample_xml_document_path():
    return '%s/%s' % (current_app.static_folder, 'SampleDocument.xml')


def get_sample_batch_doc_path(file_id):
    return '%s/%02d.pdf' % (current_app.static_folder, (int(file_id) % 10))
