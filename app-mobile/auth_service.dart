import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  // Recuperar o Token de Identidade para enviar ao backend Python
  Future<String?> obterToken() async {
    return await _auth.currentUser?.getIdToken();
  }

  // Criar usuário com E-mail e Senha (Exemplo padrão)
  Future<User?> registrarComEmail(String email, String password) async {
    try {
      UserCredential result = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      return result.user;
    } catch (e) {
      print("Erro ao criar usuário: ${e.toString()}");
      return null;
    }
  }

  // Iniciar verificação de Telefone (Para o login por SMS)
  Future<void> verificarTelefone(String phoneNumber, Function(String) codeSent) async {
    await _auth.verifyPhoneNumber(
      phoneNumber: phoneNumber,
      verificationCompleted: (PhoneAuthCredential credential) async {
        await _auth.signInWithCredential(credential);
      },
      verificationFailed: (FirebaseAuthException e) {
        print("Falha na verificação: ${e.message}");
      },
      codeSent: (String verificationId, int? resendToken) {
        codeSent(verificationId);
      },
      codeAutoRetrievalTimeout: (String verificationId) {},
    );
  }

  // Logout
  Future<void> sair() async {
    await _auth.signOut();
  }
}