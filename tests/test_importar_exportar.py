import unittest
import glob
from editor_sped import EscrituracaoICMSIPI, EscrituracaoPISCOFINS, abrir_escrituracao, EFD_ENCODING



class TestImportarExportar(unittest.TestCase):
    def test_importar_exportar_icms_ipi(self):
        for escrituracao_exemplo in glob.glob("exemplos/efd_icms_ipi_*.txt"):
            escrituracao_texto = abrir_escrituracao(escrituracao_exemplo)

            escrituracao = EscrituracaoICMSIPI(escrituracao_texto)

            resultado = escrituracao.converter_para_texto()

            with self.subTest(arquivo=escrituracao_exemplo):
                self.assertEqual(escrituracao_texto, resultado)



    def test_importar_exportar_pis_cofins(self):
        for escrituracao_exemplo in glob.glob("exemplos/efd_pis_cofins_*.txt"):
            escrituracao_texto = abrir_escrituracao(escrituracao_exemplo)

            escrituracao = EscrituracaoPISCOFINS(escrituracao_texto)

            resultado = escrituracao.converter_para_texto()

            with self.subTest(arquivo=escrituracao_exemplo):
                self.assertEqual(escrituracao_texto, resultado)



if __name__ == "__main__":
    unittest.main()
