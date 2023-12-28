import hashlib
import json


def crypto_hash(*args):
    """
    Return a sha-256 hash of the given arguments.
    """
    stringify_args = list(sorted(map(lambda data: json.dumps(data), args)))
    # creates a list of  string args like json dumps: "one", "2"
    # converts data into json type { " " }
    joined_data = ''.join(stringify_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")


if __name__ == '__main__':
    main()
