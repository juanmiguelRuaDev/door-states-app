import subprocess

def get_card_id(response_args):
    init_index = response_args.find("UID", 100)
    last_index = response_args.find('\n', init_index, init_index+35)
    if init_index < 0:
        return ''
    response = response_args[init_index:last_index-1]
    init_index = response.find(':')
    if init_index < 0:
        return ''
    response = response[init_index+1:]
    resp_spliced = response.split('  ')
    return ''.join(resp_spliced).swapcase()[:7].strip()

try:
    p = subprocess.Popen(['nfc-list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
except FileNotFoundError:
    out = None

print(get_card_id(str(out)))