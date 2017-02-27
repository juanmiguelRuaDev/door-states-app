

response = """b'nfc-list uses libnfc 1.7.1\nNFC device: ACS / ACR122U PICC Interface opened\n
    1 ISO14443A passive target(s) found:\nISO/IEC 14443A (106 kbps) target:\n    ATQA (SENS_RES): 00  04  \n
       UID (NFCID1): b7  56  04  64  \n      SAK (SEL_RES): 08  \n\n' """
print(response)
firstindex = response.find("UID", 100)
lastindex = response.find('\n', firstindex, firstindex+35)
print(firstindex)

if firstindex > 0:
    response = response[firstindex:lastindex-1]
    print(response)

firstindex = response.find(':')
if firstindex > 0:
    response = response[firstindex+1:]
    resp_splitted = response.split('  ')
    print(''.join(resp_splitted).swapcase())