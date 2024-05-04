import unittest
import glob
from editor_sped import EscrituracaoICMSIPI, EscrituracaoPISCOFINS, EFD_ENCODING



class TestImportarExportar(unittest.TestCase):
    def test_importar_exportar_icms_ipi(self):
        for exemplo in glob.glob("exemplos/efd_icms_ipi_*.txt"):
            with open(exemplo, "r", encoding=EFD_ENCODING) as arquivo:
                escrituracao_texto = arquivo.read()

                escrituracao = EscrituracaoICMSIPI(escrituracao_texto)

            resultado = escrituracao.converter_para_texto()

            with self.subTest(arquivo=exemplo):
                self.assertEqual(escrituracao_texto, resultado)



    def test_importar_exportar_pis_cofins(self):
        for exemplo in glob.glob("exemplos/efd_pis_cofins_*.txt"):
            with open(exemplo, "r", encoding=EFD_ENCODING) as arquivo:
                escrituracao_texto = arquivo.read()

                escrituracao = EscrituracaoPISCOFINS(escrituracao_texto)

            resultado = escrituracao.converter_para_texto()

            with self.subTest(arquivo=exemplo):
                self.assertEqual(escrituracao_texto, resultado)



if __name__ == "__main__":
    unittest.main()
