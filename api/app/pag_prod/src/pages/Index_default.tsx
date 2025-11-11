import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { RefreshCcw, Copy, Save, X, Trash2  } from 'lucide-react';

const url_api = "http://10.0.0.20:4000";

const Index_default = () => {
  const [listaEscalas, setListaEscalas] = useState([])
  const [escalaView, setEscalaView] = useState("")

  const pega_mensagem_escala = async(data) => {
    fetch(`${url_api}/conteudo_escala?nome_arq=${data}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição: ' + response.status);
      }
      return response.json(); // converte a resposta para JSON
    })
    .then(data => {
      if(data["existe"]) {
        setEscalaView(data["conteudo"])
      } else {
        setEscalaView('')
        toast.info(`Arquivo de escala não encontrado`);
      }
    })
    .catch(error => {
      console.error('Ocorreu um erro:', error);
    });
  }

  const pega_lista_escalas = async() => {
    fetch(`${url_api}/lista_escalas`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição: ' + response.status);
      }
      return response.json(); // converte a resposta para JSON
    })
    .then(data => {
      setListaEscalas(data["lista_arq"])
    })
    .catch(error => {
      console.error('Ocorreu um erro:', error);
    });
  }


  useEffect(() => {
    pega_lista_escalas()
  },[])

  return (
    <div className="min-h-screen bg-background p-6 space-y-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-foreground text-center">Visualizar escalas</h1>

        {/* Area do meio com lista e novo user */}
        <div className="">
          {/* Área de Botões */}
          <Card>
            <CardHeader>
              <CardTitle className="text-center">Escalas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center justify-center gap-4 m-5 max-h-[600px] overflow-y-auto p-5">
                {escalaView != '' && (
                  <div className="flex flex-col">
                    <div className="flex justify-between m-5">
                      <button className="" onClick={() => {navigator.clipboard.writeText(escalaView) ; toast.success(`Escala copiada`);}}>
                        <Copy/>
                      </button>

                      <button className="" onClick={() => {setEscalaView('')}}>
                        <X/>
                      </button>
                    </div>

                    <p></p>
                    <textarea
                      id="Escala view"
                      value={escalaView}
                      className="w-[400px] h-[450px] p-2 border rounded overflow-auto text-center"
                      onChange={(e) => {setEscalaView(e.target.value)}}
                    />

                  </div>
                )}
                {escalaView == '' && listaEscalas.length > 0 && (
                  listaEscalas.map((data, index) => (
                    <div className="m-2">
                      <button
                        className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-full shadow-md transition"
                        onClick={() => { pega_mensagem_escala(data)}}>
                        {data.replace('.json','')}
                      </button>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Index_default;
