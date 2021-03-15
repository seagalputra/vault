# 🤖 Vault

Simple application to create and sign ethereum transaction.

## Requirements
Before running the application, make sure you install the requirement below

- Python >= 3.6

## How to Run

There are several ways to run the application. The easy way to execute `install.sh` script to automatically installing dependencies and configuring script

```sh
$ chmod +x install.sh
$ install.sh
$ ./vault <path>
```

or you can follow the second way with following script

```sh
$ chmod +x vault.py
$ ./vault.py <path>
```

If you decide to use python as usual, you can install manually the dependencies as written in `requirements.txt` and run the script with python. Just follow along the bash syntax below and you good to go.

```sh
$ pip install -r requirements.txt
$ python vault.py <path>
```

After successfully run the vault application, you can execute `client.py` to run the sample request.

```sh
$ python client.py # or python3 client.py
```

## Example Request

You can use the `sample_test.txt` along with `client.py` to make request to the application or if you want to write your own request, here's the request specification.

```json
{
  "id": "some id",
  "type": "sign_transfer",
  "from_address": "ETH address",
  "to_address": "ETH address",
  "amount": "some amount"
}
```

You can use multiple message by adding new line in the `sample_test.txt` then execute again using `client.py`.

## Notes

- All the credentials such as private key is for testing purpose only. I don't provide any huge amount of ETH to broadcast the transaction and the amount only valid in testnet.
- When send message using other client such as `socat`, new line character becomes `\\n` (with double backslash) that cause issue when reading the request message. It's recommend to use `client.py` file to test the application or you can write your own client.
