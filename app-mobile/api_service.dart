import 'package:dio/dio.dart';

class ApiService {
  // Substitua pelo IP da sua máquina onde o backend FastAPI está rodando
  final String _baseUrl = 'http://192.168.3.51:8000'; 
  final Dio _dio = Dio();

  Future<Map<String, dynamic>> registrarNota({
    required String cpf,
    String? urlQr,
    String? chave,
    required String tipo,
    String? tokenFirebase, // Token obtido via AuthService
  }) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/notas/registrar',
        options: Options(headers: {
          if (tokenFirebase != null) 'Authorization': 'Bearer $tokenFirebase',
        }),
        data: {
          'cpf_usuario': cpf,
          'chave_danfe': chave,
          'url_qr': urlQr,
          'tipo': tipo,
        },
      );
      return response.data;
    } on DioException catch (e) {
      final erro = e.response?.data['detail'] ?? 'Erro desconhecido no servidor';
      throw Exception(erro);
    }
  }

  Future<Map<String, dynamic>> buscarCupons(String cpf) async {
    try {
      final response = await _dio.get('$_baseUrl/usuarios/$cpf/cupons');
      return response.data;
    } on DioException catch (e) {
      final erro = e.response?.data['detail'] ?? 'Não foi possível carregar seus cupons.';
      throw Exception(erro);
    }
  }
}