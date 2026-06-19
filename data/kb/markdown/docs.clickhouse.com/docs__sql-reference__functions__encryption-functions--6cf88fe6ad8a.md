# Encryption functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Encryption
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/encryption-functions.md)# Encryption functions

These functions implement encryption and decryption of data with AES (Advanced Encryption Standard) algorithm.


The key length depends on the encryption mode: `16`, `24`, and `32` bytes long for `-128-`, `-196-`, and `-256-` modes respectively.


The initialization vector length is always 16 bytes (bytes in excess of 16 are ignored).


## HMAC[​](#HMAC "Direct link to HMAC")


Introduced in: v25\.12\.0


Computes the HMAC (Hash\-based Message Authentication Code) for the given message using the specified hash algorithm and secret key.


Supported hash algorithms:


- blake2b512
- blake2s256
- md4
- md5
- md5\-sha1
- mdc2
- ripemd (aliases: RIPEMD160, ripemd)
- ripemd160
- rmd160 (aliases: RIPEMD160, rmd160\)
- sha1
- sha224
- sha256
- sha3\-224
- sha3\-256
- sha3\-384
- sha3\-512
- sha384
- sha512
- sha512\-224
- sha512\-256
- shake128
- shake256
- sm3
- ssl3\-md5 (aliases: MD5, ssl3\-md5\)
- ssl3\-sha1 (aliases: SHA1, ssl3\-sha1\)
- whirlpool


**Syntax**



```
HMAC(mode, message, key)

```

**Arguments**


- `mode` — Hash algorithm name (case\-insensitive). Supported: md5, sha1, sha224, sha256, sha384, sha512\. [`String`](/docs/sql-reference/data-types/string)
- `message` — Message to be authenticated. [`String`](/docs/sql-reference/data-types/string)
- `key` — Secret key for HMAC. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a binary string containing the HMAC digest. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic HMAC\-SHA256**



```
SELECT hex(HMAC('sha256', 'The quick brown fox jumps over the lazy dog', 'secret_key'));

```


```
┌─hex(HMAC('sha256', 'The quick brown fox jumps over the lazy dog', 'secret_key'))─┐
│ 31FD15FA0F61FD40DC09D919D4AA5B4141A0B27C1D51E74A6789A890AAAA187C                 │
└──────────────────────────────────────────────────────────────────────────────────┘

```

**Different hash algorithms**



```
SELECT
    hex(HMAC('md5', 'message', 'key')) AS hmac_md5,
    hex(HMAC('sha1', 'message', 'key')) AS hmac_sha1,
    hex(HMAC('sha256', 'message', 'key')) AS hmac_sha256;

```


```
┌─hmac_md5─────────────────────────┬─hmac_sha1────────────────────────────────┬─hmac_sha256──────────────────────────────────────────────────────┐
│ 4E4748E62B463521F6775FBF921234B5 │ 2088DF74D5F2146B48146CAF4965377E9D0BE3A4 │ 6E9EF29B75FFFC5B7ABAE527D58FDADB2FE42E7219011976917343065F58ED4A │
└──────────────────────────────────┴──────────────────────────────────────────┴──────────────────────────────────────────────────────────────────┘

```

**Case\-insensitive mode**



```
SELECT
    hmac('SHA256', 'message', 'key') = HMAC('sha256', 'message', 'key') AS same_result,
    HMAC('SHA256', 'message', 'key') = Hmac('Sha256', 'message', 'key') AS also_same;

```


```
┌─same_result─┬─also_same─┐
│           1 │         1 │
└─────────────┴───────────┘

```

## aes\_decrypt\_mysql[​](#aes_decrypt_mysql "Direct link to aes_decrypt_mysql")


Introduced in: v20\.12\.0


Decrypts data encrypted by MySQL's [`AES_ENCRYPT`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-encrypt) function.


Produces the same plaintext as [`decrypt`](#decrypt) for the same inputs.
When `key` or `iv` are longer than they should normally be, `aes_decrypt_mysql` will stick to what MySQL's `aes_decrypt` does which is to 'fold' `key` and ignore the excess bits of `IV`.


Supports the following decryption modes:


- aes\-128\-ecb, aes\-192\-ecb, aes\-256\-ecb
- aes\-128\-cbc, aes\-192\-cbc, aes\-256\-cbc
- aes\-128\-cfb128
- aes\-128\-ofb, aes\-192\-ofb, aes\-256\-ofb


**Syntax**



```
aes_decrypt_mysql(mode, ciphertext, key[, iv])

```

**Arguments**


- `mode` — Decryption mode. [`String`](/docs/sql-reference/data-types/string)
- `ciphertext` — Encrypted text that needs to be decrypted. [`String`](/docs/sql-reference/data-types/string)
- `key` — Decryption key. [`String`](/docs/sql-reference/data-types/string)
- `iv` — Optional. Initialization vector. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the decrypted String. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Decrypt MySQL data**



```
-- Let's decrypt data we've previously encrypted with MySQL:
mysql> SET  block_encryption_mode='aes-256-ofb';
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT aes_encrypt('Secret', '123456789101213141516171819202122', 'iviviviviviviviv123456') as ciphertext;
+------------------------+
| ciphertext             |
+------------------------+
| 0x24E9E4966469         |
+------------------------+
1 row in set (0.00 sec)

SELECT aes_decrypt_mysql('aes-256-ofb', unhex('24E9E4966469'), '123456789101213141516171819202122', 'iviviviviviviviv123456') AS plaintext

```


```
┌─plaintext─┐
│ Secret    │
└───────────┘

```

## aes\_encrypt\_mysql[​](#aes_encrypt_mysql "Direct link to aes_encrypt_mysql")


Introduced in: v20\.12\.0


Encrypts text the same way as MySQL's `AES_ENCRYPT` function does.
The resulting ciphertext can be decrypted with MySQL's `AES_DECRYPT` function.
Produces the same ciphertext as the `encrypt` function for the same inputs.
When `key` or `iv` are longer than they should normally be, `aes_encrypt_mysql` will stick to what MySQL's `aes_encrypt` does which is to 'fold' `key` and ignore the excess bits of `iv`.


The supported encryption modes are:


- aes\-128\-ecb, aes\-192\-ecb, aes\-256\-ecb
- aes\-128\-cbc, aes\-192\-cbc, aes\-256\-cbc
- aes\-128\-ofb, aes\-192\-ofb, aes\-256\-ofb


**Syntax**



```
aes_encrypt_mysql(mode, plaintext, key[, iv])

```

**Arguments**


- `mode` — Encryption mode. [`String`](/docs/sql-reference/data-types/string)
- `plaintext` — Text that should be encrypted. [`String`](/docs/sql-reference/data-types/string)
- `key` — Encryption key. If the key is longer than required by `mode`, MySQL\-specific key folding is performed. [`String`](/docs/sql-reference/data-types/string)
- `iv` — Optional. Initialization vector. Only the first 16 bytes are taken into account. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Ciphertext binary string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Equal input comparison**



```
-- Given equal input encrypt and aes_encrypt_mysql produce the same ciphertext:
SELECT encrypt('aes-256-ofb', 'Secret', '12345678910121314151617181920212', 'iviviviviviviviv') = aes_encrypt_mysql('aes-256-ofb', 'Secret', '12345678910121314151617181920212', 'iviviviviviviviv') AS ciphertexts_equal;

```


```
┌─ciphertexts_equal─┐
│                 1 │
└───────────────────┘

```

**Encrypt fails with long key**



```
-- But encrypt fails when key or iv is longer than expected:
SELECT encrypt('aes-256-ofb', 'Secret', '123456789101213141516171819202122', 'iviviviviviviviv123');

```


```
Received exception from server (version 22.6.1):
Code: 36. DB::Exception: Received from localhost:9000. DB::Exception: Invalid key size: 33 expected 32: While processing encrypt('aes-256-ofb', 'Secret', '123456789101213141516171819202122', 'iviviviviviviviv123').

```

**MySQL compatibility**



```
-- aes_encrypt_mysql produces MySQL-compatible output:
SELECT hex(aes_encrypt_mysql('aes-256-ofb', 'Secret', '123456789101213141516171819202122', 'iviviviviviviviv123')) AS ciphertext;

```


```
┌─ciphertext───┐
│ 24E9E4966469 │
└──────────────┘

```

**Longer IV produces the same result**



```
-- Notice how supplying even longer IV produces the same result
SELECT hex(aes_encrypt_mysql('aes-256-ofb', 'Secret', '123456789101213141516171819202122', 'iviviviviviviviv123456')) AS ciphertext

```


```
┌─ciphertext───┐
│ 24E9E4966469 │
└──────────────┘

```

## decrypt[​](#decrypt "Direct link to decrypt")


Introduced in: v20\.12\.0


This function decrypts an AES\-encrypted binary string using the following modes:


- aes\-128\-ecb, aes\-192\-ecb, aes\-256\-ecb
- aes\-128\-cbc, aes\-192\-cbc, aes\-256\-cbc
- aes\-128\-ofb, aes\-192\-ofb, aes\-256\-ofb
- aes\-128\-gcm, aes\-192\-gcm, aes\-256\-gcm
- aes\-128\-ctr, aes\-192\-ctr, aes\-256\-ctr
- aes\-128\-cfb, aes\-128\-cfb1, aes\-128\-cfb8


**Syntax**



```
decrypt(mode, ciphertext, key[, iv, aad])

```

**Arguments**


- `mode` — Decryption mode. [`String`](/docs/sql-reference/data-types/string)
- `ciphertext` — Encrypted text that should be decrypted. [`String`](/docs/sql-reference/data-types/string)
- `key` — Decryption key. [`String`](/docs/sql-reference/data-types/string)
- `iv` — Initialization vector. Required for `-gcm` modes, optional for others. [`String`](/docs/sql-reference/data-types/string)
- `aad` — Additional authenticated data. Won't decrypt if this value is incorrect. Works only in `-gcm` modes, for others throws an exception. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns decrypted plaintext. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Correctly decrypting encrypted data**



```
-- Re-using the table from the encrypt function example
SELECT comment, hex(secret) FROM encryption_test;

```


```
┌─comment──────────────┬─hex(secret)──────────────────────────────────┐
│ aes-256-gcm          │ A8A3CCBC6426CFEEB60E4EAE03D3E94204C1B09E0254 │
│ aes-256-gcm with AAD │ A8A3CCBC6426D9A1017A0A932322F1852260A4AD6837 │
└──────────────────────┴──────────────────────────────────────────────┘
┌─comment──────────────────────────┬─hex(secret)──────────────────────┐
│ aes-256-ofb no IV                │ B4972BDC4459                     │
│ aes-256-ofb no IV, different key │ 2FF57C092DC9                     │
│ aes-256-ofb with IV              │ 5E6CB398F653                     │
│ aes-256-cbc no IV                │ 1BC0629A92450D9E73A00E7D02CF4142 │
└──────────────────────────────────┴──────────────────────────────────┘

```

**Incorrectly decrypting encrypted data**



```
SELECT comment, decrypt('aes-256-cfb128', secret, '12345678910121314151617181920212') AS plaintext FROM encryption_test

```


```
-- Notice how only a portion of the data was properly decrypted, and the rest is gibberish since either `mode`, `key`, or `iv` were different upon encryption.
┌─comment──────────────┬─plaintext──┐
│ aes-256-gcm          │ OQ�E
                             �t�7T�\���\�   │
│ aes-256-gcm with AAD │ OQ�E
                             �\��si����;�o�� │
└──────────────────────┴────────────┘
┌─comment──────────────────────────┬─plaintext─┐
│ aes-256-ofb no IV                │ Secret    │
│ aes-256-ofb no IV, different key │ �4�
                                        �         │
│ aes-256-ofb with IV              │ ���6�~        │
│aes-256-cbc no IV                │ �2*4�h3c�4w��@
└──────────────────────────────────┴───────────┘

```

## encrypt[​](#encrypt "Direct link to encrypt")


Introduced in: v20\.12\.0


Encrypts plaintext into ciphertext using AES in one of the following modes:


- aes\-128\-ecb, aes\-192\-ecb, aes\-256\-ecb
- aes\-128\-cbc, aes\-192\-cbc, aes\-256\-cbc
- aes\-128\-ofb, aes\-192\-ofb, aes\-256\-ofb
- aes\-128\-gcm, aes\-192\-gcm, aes\-256\-gcm
- aes\-128\-ctr, aes\-192\-ctr, aes\-256\-ctr
- aes\-128\-cfb, aes\-128\-cfb1, aes\-128\-cfb8


**Syntax**



```
encrypt(mode, plaintext, key[, iv, aad])

```

**Arguments**


- `mode` — Encryption mode. [`String`](/docs/sql-reference/data-types/string)
- `plaintext` — Text that should be encrypted. [`String`](/docs/sql-reference/data-types/string)
- `key` — Encryption key. [`String`](/docs/sql-reference/data-types/string)
- `iv` — Initialization vector. Required for `-gcm` modes, optional for others. [`String`](/docs/sql-reference/data-types/string)
- `aad` — Additional authenticated data. It isn't encrypted, but it affects decryption. Works only in `-gcm` modes, for others it throws an exception. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns binary string ciphertext. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Example encryption**



```
CREATE TABLE encryption_test
(
    `comment` String,
    `secret` String
)
ENGINE = MergeTree;

INSERT INTO encryption_test VALUES
('aes-256-ofb no IV', encrypt('aes-256-ofb', 'Secret', '12345678910121314151617181920212')),
('aes-256-ofb no IV, different key', encrypt('aes-256-ofb', 'Secret', 'keykeykeykeykeykeykeykeykeykeyke')),
('aes-256-ofb with IV', encrypt('aes-256-ofb', 'Secret', '12345678910121314151617181920212', 'iviviviviviviviv')),
('aes-256-cbc no IV', encrypt('aes-256-cbc', 'Secret', '12345678910121314151617181920212'));

SELECT comment, hex(secret) FROM encryption_test;

```


```
┌─comment──────────────────────────┬─hex(secret)──────────────────────┐
│ aes-256-ofb no IV                │ B4972BDC4459                     │
│ aes-256-ofb no IV, different key │ 2FF57C092DC9                     │
│ aes-256-ofb with IV              │ 5E6CB398F653                     │
│ aes-256-cbc no IV                │ 1BC0629A92450D9E73A00E7D02CF4142 │
└──────────────────────────────────┴──────────────────────────────────┘

```

**Example with GCM mode**



```
INSERT INTO encryption_test VALUES
('aes-256-gcm', encrypt('aes-256-gcm', 'Secret', '12345678910121314151617181920212', 'iviviviviviviviv')),

('aes-256-gcm with AAD', encrypt('aes-256-gcm', 'Secret', '12345678910121314151617181920212', 'iviviviviviviviv', 'aad'));

SELECT comment, hex(secret) FROM encryption_test WHERE comment LIKE '%gcm%';

```


```
┌─comment──────────────┬─hex(secret)──────────────────────────────────┐
│ aes-256-gcm          │ A8A3CCBC6426CFEEB60E4EAE03D3E94204C1B09E0254 │
│ aes-256-gcm with AAD │ A8A3CCBC6426D9A1017A0A932322F1852260A4AD6837 │
└──────────────────────┴──────────────────────────────────────────────┘

```

## tryDecrypt[​](#tryDecrypt "Direct link to tryDecrypt")


Introduced in: v22\.10\.0


Similar to the `decrypt` function, but returns `NULL` if decryption fails when using the wrong key.


**Syntax**



```
tryDecrypt(mode, ciphertext, key[, iv, aad])

```

**Arguments**


- `mode` — Decryption mode. [`String`](/docs/sql-reference/data-types/string)
- `ciphertext` — Encrypted text that should be decrypted. [`String`](/docs/sql-reference/data-types/string)
- `key` — Decryption key. [`String`](/docs/sql-reference/data-types/string)
- `iv` — Optional. Initialization vector. Required for `-gcm` modes, optional for other modes. [`String`](/docs/sql-reference/data-types/string)
- `aad` — Optional. Additional authenticated data. Won't decrypt if this value is incorrect. Works only in `-gcm` modes, for other modes throws an exception. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the decrypted String, or `NULL` if decryption fails. [`Nullable(String)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Create table and insert data**



```
-- Let's create a table where user_id is the unique user id, encrypted is an encrypted string field, iv is an initial vector for decrypt/encrypt.
-- Assume that users know their id and the key to decrypt the encrypted field:
CREATE TABLE decrypt_null
(
    dt DateTime,
    user_id UInt32,
    encrypted String,
    iv String
)
ENGINE = MergeTree;

-- Insert some data:
INSERT INTO decrypt_null VALUES
('2022-08-02 00:00:00', 1, encrypt('aes-256-gcm', 'value1', 'keykeykeykeykeykeykeykeykeykey01', 'iv1'), 'iv1'),
('2022-09-02 00:00:00', 2, encrypt('aes-256-gcm', 'value2', 'keykeykeykeykeykeykeykeykeykey02', 'iv2'), 'iv2'),
('2022-09-02 00:00:01', 3, encrypt('aes-256-gcm', 'value3', 'keykeykeykeykeykeykeykeykeykey03', 'iv3'), 'iv3');

-- Try decrypt with one key
SELECT
    dt,
    user_id,
    tryDecrypt('aes-256-gcm', encrypted, 'keykeykeykeykeykeykeykeykeykey02', iv) AS value
FROM decrypt_null
ORDER BY user_id ASC

```


```
┌──────────────────dt─┬─user_id─┬─value──┐
│ 2022-08-02 00:00:00 │       1 │ ᴺᵁᴸᴸ   │
│ 2022-09-02 00:00:00 │       2 │ value2 │
│ 2022-09-02 00:00:01 │       3 │ ᴺᵁᴸᴸ   │
└─────────────────────┴─────────┴────────┘

```
[PreviousEncoding](/docs/sql-reference/functions/encoding-functions)[NextDictionaries](/docs/sql-reference/functions/ext-dict-functions)- [HMAC](#HMAC)- [aes\_decrypt\_mysql](#aes_decrypt_mysql)- [aes\_encrypt\_mysql](#aes_encrypt_mysql)- [decrypt](#decrypt)- [encrypt](#encrypt)- [tryDecrypt](#tryDecrypt)
Was this page helpful?
