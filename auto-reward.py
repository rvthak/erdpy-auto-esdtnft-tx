import csv
import os

# ---------------------------------- Arguments ----------------------------------

INPUT_CSV = 'rewardData.csv'
TOKEN_HEX = '4C4B4D45582D616162393130'
TOKEN_NONCE = '22e4ef'
SENDER_ADDR = 'erd1en90783mdh9kt928qfrt35e7lzqsu9h557j24p3lreu9alkc094qsy4z52'
PEM = 'wallet-owner.pem'
GAS_LIMIT = str(500000)
PROXY = 'https://gateway.elrond.com'
CHAIN = '1'
EGLD_VAL = 1000000000000000000

# ---------------------------------- Functions ----------------------------------

# Convert a csv MEX value to elrond compatible hex value
def elrondHex(decstr):
	return evenHex( str(hex(int(decstr))).replace("0x", ""))

def evenHex(hex):
	if( len(hex)%2==1 ):
		hex = '0' + hex
	return hex

def bech32toHex(addr):
	return str(os.popen("erdpy wallet bech32 --decode " + addr + \
	" | sed 's/^.*= //'").read())

# Builds an erdpy transaction using the given arguments
def buildErdTx(addr, amount):
	return 'erdpy tx new' + \
	' --pem ' + PEM + \
	' --recall-nonce' + \
	' --receiver ' + SENDER_ADDR + \
	' --value 0' + \
	' --gas-limit ' + GAS_LIMIT + \
	' --send' + \
	' --wait-result' + \
	' --outfile ' + './reports/' + addr + '.report.json' + \
	' --proxy ' + PROXY + \
	' --chain ' + CHAIN + \
	' --data ' + 'ESDTNFTTransfer@' + TOKEN_HEX + '@'+ TOKEN_NONCE + \
	'@' + elrondHex(int(amount)*EGLD_VAL) + '@' + bech32toHex(addr)

# -------------------------------------------------------------------------------

# Open and parse the csv file
file = open(INPUT_CSV)
csvreader = csv.reader(file)
rows = []
for row in csvreader:
	rows.append(row)

# Create the reports directory
os.system("mkdir reports")

# Distribute the rewards
print("\n (i) Distributing rewards to Investors...")
for i, row in enumerate(rows):
	print("\n  " + str(i+1) + ". " + row[0] + " - " + row[1] + " MEX")
	os.system( buildErdTx( row[0], row[1]) )

print( "\n (i) Reward distribution complete\n")
