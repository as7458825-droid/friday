import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.File;

public class VaultEncryptor {
    private static final String ALGORITHM = "AES";

    public static void main(String[] args) {
        if (args.length < 3) {
            System.out.println("Usage: java VaultEncryptor <encrypt|decrypt> <text> <key_path>");
            return;
        }

        String mode = args[0];
        String data = args[1];
        String keyPath = args[2];

        try {
            if (mode.equals("encrypt")) {
                String encrypted = encrypt(data, keyPath);
                System.out.println("RESULT:" + encrypted);
            } else if (mode.equals("decrypt")) {
                String decrypted = decrypt(data, keyPath);
                System.out.println("RESULT:" + decrypted);
            }
        } catch (Exception e) {
            System.out.println("ERROR:" + e.getMessage());
        }
    }

    private static String encrypt(String data, String keyPath) throws Exception {
        byte[] keyBytes;
        if (new File(keyPath).exists()) {
            keyBytes = Files.readAllBytes(Paths.get(keyPath));
        } else {
            KeyGenerator keyGen = KeyGenerator.getInstance(ALGORITHM);
            keyGen.init(256);
            SecretKey secretKey = keyGen.generateKey();
            keyBytes = secretKey.getEncoded();
            Files.write(Paths.get(keyPath), keyBytes);
        }

        SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, ALGORITHM);
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);
        byte[] encryptedBytes = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    private static String decrypt(String encryptedData, String keyPath) throws Exception {
        byte[] keyBytes = Files.readAllBytes(Paths.get(keyPath));
        SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, ALGORITHM);
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, secretKeySpec);
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(encryptedData));
        return new String(decryptedBytes);
    }
}
