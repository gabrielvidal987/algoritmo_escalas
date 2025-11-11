import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox"
import { toast } from "sonner";
import { RefreshCcw, Copy, Save, X, Trash2  } from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ScrollArea } from "@/components/ui/scroll-area";


interface TableDataMusic {
  Nome: string;
  Instrumentista: boolean;
  Instrumento: string;
  Vocalista: boolean;
  "Tipo Vocal": string;
  "Faz mensagem musical": string;
  "Dias não preferenciais": [];
  "Dias preferenciais": [];
  Genero: string;
  Atuando: boolean;
}

const url_api = "http://10.0.0.20:4000";

const Index = () => {
  const [formData, setFormData] = useState({
    Nome: "",
    Instrumentista: false,
    Instrumento: "Nenhum",
    Vocalista: false,
    "Tipo Vocal": "Desconhecido",
    "Faz mensagem musical": false,
    "Dias não preferenciais": [],
    "Dias preferenciais": [],
    Genero: "",
    Atuando: false,
  });
  const [formNewEscale, setFormNewEscale] = useState({
    Nome: "",
    Mes: 0,
    Ano: 0,
    SepararGenero: false,
    Domingo : 0,
    Segunda : 0,
    Terca : 0,
    Quarta : 0,
    Quinta : 0,
    Sexta : 0,
    Sabado : 0,
  });
  const [tableUsers, setTableUsers] = useState<TableDataMusic[]>([])
  const [listaEscalas, setListaEscalas] = useState([])
  const [escalaView, setEscalaView] = useState("")
  const [selectedFile, setSelectedFile] = useState("")

  const marca_dia = (campo, valor, dia_semana, func_set_data, data_to_alter) => {
    if (valor) {
      // Adiciona dia_semana ao array, se ainda não estiver
      func_set_data({
        ...data_to_alter,
        [campo]: [...data_to_alter[campo], dia_semana]
      });
    } else {
      // Remove dia_semana do array
      func_set_data({
        ...data_to_alter,
        [campo]: data_to_alter[campo].filter(d => d !== dia_semana)
      });
    }
  }

  const pega_usuarios_musica = async() => {
    fetch(`${url_api}/lista_user_music`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição: ' + response.status);
      }
      return response.json(); // converte a resposta para JSON
    })
    .then(data => {
      // console.log(data["lista_user_music"])
      setTableUsers(data["lista_user_music"])
    })
    .catch(error => {
      console.error('Ocorreu um erro:', error);
    });
  }


  const deleteEscale = async(data) => {
    fetch(`${url_api}/deletar_escala?nome_arq=${data}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição: ' + response.status);
      }
      return response.json(); // converte a resposta para JSON
    })
    .then(data => {
      if(!data["existe"]) {
        toast.success(`Escala deletada com sucesso`);
        window.location.href = ''
      } else {
        toast.info(`Escala deletada sem sucesso`);
      }
    })
    .catch(error => {
      console.error('Ocorreu um erro:', error);
    });
  }

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

  const salvar_mensagem = async() => {
    fetch(`${url_api}/salvar_alteracao`, {
      method: 'POST', // 👈 método POST
      headers: {
        'Content-Type': 'application/json', // 👈 avisa que o corpo é JSON
      },
      body: JSON.stringify({
        "file" : selectedFile,
        "conteudo" : {escala : escalaView}
      }), // 👈 corpo da requisição
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição: ' + response.status);
      }
      return response.json(); // converte a resposta para JSON
    })
    .then(data => {
      if (data.sucess) {
        toast.success("Salvo com sucesso o conteúdo da escala")
      } else {
        toast.error("Sem sucesso ao salvar o conteúdo da escala")
      }
    })
    .catch(error => {
      console.error('Ocorreu um erro:', error);
    });
  }

  const gerar_escala = async() => {
    fetch(`${url_api}/gerar_escala_musica`, {
      method: 'POST', // 👈 método POST
      headers: {
        'Content-Type': 'application/json', // 👈 avisa que o corpo é JSON
      },
      body: JSON.stringify(formNewEscale), // 👈 corpo da requisição
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição: ' + response.status);
      }
      return response.json(); // converte a resposta para JSON
    })
    .then(data => {
      console.log(data)
    })
    .catch(error => {
      console.error('Ocorreu um erro:', error);
    });
  }

  const add_usuario_musica = async() => {
    fetch(`${url_api}/add_user_music`, {
      method: 'POST', // 👈 método POST
      headers: {
        'Content-Type': 'application/json', // 👈 avisa que o corpo é JSON
      },
      body: JSON.stringify(formData), // 👈 corpo da requisição
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição: ' + response.status);
      }
      return response.json(); // converte a resposta para JSON
    })
    .then(data => {
      console.log(data)
      setFormData({
        Nome: "",
        Instrumentista: false,
        Instrumento: "Nenhum",
        Vocalista: false,
        "Tipo Vocal": "Desconhecido",
        "Faz mensagem musical": false,
        "Dias não preferenciais": [],
        "Dias preferenciais": [],
        Genero: "",
        Atuando: false,
      });
    })
    .catch(error => {
      console.error('Ocorreu um erro:', error);
    });
  }

  useEffect(() => {
    pega_usuarios_musica()
    pega_lista_escalas()
  },[])

  return (
    <div className="min-h-screen bg-background p-6 space-y-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-foreground">Sistema de Gestão</h1>

        {/* Tabela com Scroll */}
        <Card>
          <CardHeader>
            <CardTitle className="flex justify-between pl-5 pr-5">
              Membros
              <button onClick={(e) => {window.location.href = ''}}>
                <RefreshCcw className="ml-5"/>
              </button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto w-full rounded-md border border-border">
              <ScrollArea className="h-[300px] min-w-[500px]">
                <Table className="">
                  <TableHeader className="sticky top-0 bg-table-header z-10">
                    <TableRow>
                      <TableHead className="w-[50px]">Atuando</TableHead>
                      <TableHead className="text-center">Nome</TableHead>
                      <TableHead className="text-center">Vocalista</TableHead>
                      <TableHead className="text-center">Tipo Vocal</TableHead>
                      <TableHead className="text-center">Instrumentista</TableHead>
                      <TableHead className="text-center">Instrumento</TableHead>
                      <TableHead className="text-center">Faz Mensagem Musical</TableHead>
                      <TableHead className="text-center">Dias Não Preferenciais</TableHead>
                      <TableHead className="text-center">Dias Preferenciais</TableHead>
                      <TableHead className="text-center">Genero</TableHead>
                    </TableRow>
                  </TableHeader>
                  {tableUsers && tableUsers.length > 0 ? (
                    <TableBody>
                      {tableUsers.map((item, index) => (
                        <TableRow key={index} className="hover:bg-table-row-hover transition-colors">
                          <TableCell className="font-medium text-center">{item.Atuando ? "Sim" : "Não"}</TableCell>
                          <TableCell className="text-center">{item.Nome}</TableCell>
                          <TableCell className="text-center">{item.Vocalista ? "Sim" : "Não"}</TableCell>
                          <TableCell className="text-center">{item["Tipo Vocal"]}</TableCell>
                          <TableCell className="text-center">{item.Instrumentista ? "Sim" : "Não"}</TableCell>
                          <TableCell className="text-center">{item.Instrumento}</TableCell>
                          <TableCell className="text-center">{item["Faz mensagem musical"] ? "Sim" : "Não"}</TableCell>
                          <TableCell className="text-center">{item["Dias não preferenciais"].join(", ")}</TableCell>
                          <TableCell className="text-center">{item["Dias preferenciais"].join(", ")}</TableCell>
                          <TableCell className="text-center">{item.Genero}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                    ) : (
                    <TableBody>
                      <TableRow>
                        <TableCell colSpan={10} className="text-center text-gray-500 py-4">
                          Nenhum registro encontrado
                        </TableCell>
                      </TableRow>
                    </TableBody>
                    )
                  }
                </Table>
              </ScrollArea>
            </div>
          </CardContent>
        </Card>

        {/* Area do meio com lista e novo user */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Área de Botões */}
          <Card>
            <CardHeader>
              <CardTitle className="text-center">Escalas geradas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center justify-center gap-4 m-5 max-h-[600px] overflow-y-auto p-5">
                {escalaView != '' && (
                  <div className="flex flex-col">
                    <div className="flex justify-between m-5">
                      <button className="" onClick={() => {navigator.clipboard.writeText(escalaView) ; toast.success(`Escala copiada`);}}>
                        <Copy/>
                      </button>
                      <button className="" onClick={() => {salvar_mensagem()}}>
                        <Save/>
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
                        onClick={() => {setSelectedFile(data) ; pega_mensagem_escala(data)}}>
                        {data.replace('.json','')}
                      </button>
                      <button 
                        className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-full shadow-md transition"
                        onClick={() => {deleteEscale(data)}}>
                        <Trash2/>
                      </button>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>

          {/* Formulário */}
          <Card>
            <CardHeader>
              <CardTitle className="text-center">Cadastro</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="">
                <form onSubmit={add_usuario_musica} className="space-y-6">
                  <div className="">
                    <Checkbox
                      id="Atuando"
                      onCheckedChange={(e) => setFormData({ ...formData, Atuando: Boolean(e) })}
                      className="m-1"
                    />
                    <Label htmlFor="Atuando" className="m-1">Atuando</Label>
                  </div>
                  <div className="">
                    <Checkbox
                      id="masculino"
                      onChange={(e) => setFormData({ ...formData, Genero: "m" })}
                      className="m-1"
                    />
                    <Label htmlFor="masculino" className="m-1">Masculino</Label>
                    <Checkbox
                      id="feminino"
                      onChange={(e) => setFormData({ ...formData, Genero: "f" })}
                      className="m-1"
                    />
                    <Label htmlFor="feminino" className="m-1">Feminino</Label>
                  </div>
                  <div className="">
                    <Label htmlFor="Nome">Nome</Label>
                    <Input
                      id="Nome"
                      placeholder="Nome e Sobrenome"
                      value={formData.Nome}
                      onChange={(e) => setFormData({ ...formData, Nome: e.target.value })}
                      required
                    />
                  </div>
                  <div className="">
                    <Checkbox
                      id="Instrumentista"
                      onCheckedChange={(e) => {setFormData({ ...formData, Instrumentista: Boolean(e) })}}
                      className="m-1"
                    />
                    <Label htmlFor="Instrumentista" className="m-1">Instrumentista</Label>
                  </div>
                  {formData["Instrumentista"] && (
                    <div className="space-y-2">
                      <Label htmlFor="Instrumento">Instrumento</Label>
                      <Input
                        id="Instrumento"
                        placeholder="Piano, Guitarra, Violão"
                        value={formData.Instrumento}
                        onChange={(e) => setFormData({ ...formData, Instrumento: e.target.value })}
                      />
                    </div>
                  )}
                  <div className="">
                    <Checkbox
                      id="Vocalista"
                      onCheckedChange={(e) => {setFormData({ ...formData, Vocalista: Boolean(e) })}}
                      className="m-1"
                    />
                    <Label htmlFor="Vocalista" className="m-1">Vocalista</Label>
                  </div>
                  {formData["Vocalista"] && (
                    <div className="space-y-2">
                      <Label htmlFor="Tipo Vocal">Tipo Vocal</Label>
                      <Input
                        id="Tipo Vocal"
                        placeholder="Soprano, Baritono, Tenor, Mezo masculino, Mezo feminino, Contralto"
                        value={formData["Tipo Vocal"]}
                        onChange={(e) => setFormData({ ...formData, "Tipo Vocal": e.target.value })}
                      />
                    </div>
                  )}
                  <div className="">
                    <Checkbox
                      id="Faz mensagem musical"
                      onCheckedChange={(e) => {setFormData({ ...formData, "Faz mensagem musical": Boolean(e) })}}
                      className="m-1"
                    />
                    <Label htmlFor="Faz mensagem musical" className="m-1">Faz mensagem musical</Label>
                  </div>
                  <div className="p-1">
                    <p className="mb-2"><Label className="m-5">Dias Não Preferenciais</Label></p>
                    <Checkbox
                      id="Segunda-naoPrefere"
                      onCheckedChange={(e) => {marca_dia("Dias não preferenciais", Boolean(e), "segunda", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Segunda-naoPrefere" className="m-1">Segunda</Label>
                    <Checkbox
                      id="Terça-naoPrefere"
                      onCheckedChange={(e) => {marca_dia("Dias não preferenciais", Boolean(e), "terca", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Terça-naoPrefere" className="m-1">Terça</Label>
                    <Checkbox
                      id="Quarta-naoPrefere"
                      onCheckedChange={(e) => {marca_dia("Dias não preferenciais", Boolean(e), "quarta", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Quarta-naoPrefere" className="m-1">Quarta</Label>
                    <Checkbox
                      id="Quinta-naoPrefere"
                      onCheckedChange={(e) => {marca_dia("Dias não preferenciais", Boolean(e), "quinta", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Quinta-naoPrefere" className="m-1">Quinta</Label>
                    <Checkbox
                      id="Sexta-naoPrefere"
                      onCheckedChange={(e) => {marca_dia("Dias não preferenciais", Boolean(e), "sexta", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Sexta-naoPrefere" className="m-1">Sexta</Label>
                    <Checkbox
                      id="Sábado-naoPrefere"
                      onCheckedChange={(e) => {marca_dia("Dias não preferenciais", Boolean(e), "sabado", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Sábado-naoPrefere" className="m-1">Sábado</Label>
                    <Checkbox
                      id="Domingo-naoPrefere"
                      onCheckedChange={(e) => {marca_dia("Dias não preferenciais", Boolean(e), "domingo", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Domingo-naoPrefere" className="m-1">Domingo</Label>
                  </div>
                  <div className="p-1">
                    <p className="mb-2"><Label className="m-5">Dias Preferenciais</Label></p>
                    <Checkbox
                      id="Segunda-Prefere"
                      onCheckedChange={(e) => {marca_dia("Dias preferenciais", Boolean(e), "segunda", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Segunda-Prefere" className="m-1">Segunda</Label>
                    <Checkbox
                      id="Terça-Prefere"
                      onCheckedChange={(e) => {marca_dia("Dias preferenciais", Boolean(e), "terca", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Terça-Prefere" className="m-1">Terça</Label>
                    <Checkbox
                      id="Quarta-Prefere"
                      onCheckedChange={(e) => {marca_dia("Dias preferenciais", Boolean(e), "quarta", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Quarta-Prefere" className="m-1">Quarta</Label>
                    <Checkbox
                      id="Quinta-Prefere"
                      onCheckedChange={(e) => {marca_dia("Dias preferenciais", Boolean(e), "quinta", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Quinta-Prefere" className="m-1">Quinta</Label>
                    <Checkbox
                      id="Sexta-Prefere"
                      onCheckedChange={(e) => {marca_dia("Dias preferenciais", Boolean(e), "sexta", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Sexta-Prefere" className="m-1">Sexta</Label>
                    <Checkbox
                      id="Sábado-Prefere"
                      onCheckedChange={(e) => {marca_dia("Dias preferenciais", Boolean(e), "sabado", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Sábado-Prefere" className="m-1">Sábado</Label>
                    <Checkbox
                      id="Domingo-Prefere"
                      onCheckedChange={(e) => {marca_dia("Dias preferenciais", Boolean(e), "domingo", setFormData, formData)}}
                      className="m-1"
                    />
                    <Label htmlFor="Domingo-Prefere" className="m-1">Domingo</Label>
                  </div>
                  
                  <Button type="submit" className="w-full">
                    Enviar
                  </Button>
                </form>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex justify-center pl-5 pr-5">
              Gerar escala
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[350px] rounded-md border border-border p-5 flex-col justify-center ">
              <div className="flex justify-center mb-10 gap-10">
                <Label htmlFor="Nome escala">Nome da escala</Label>
                <Input
                  id="Nome escala"
                  placeholder="Escala de dezembro"
                  required
                  className="max-w-[200px]"
                  onChange={(e) => setFormNewEscale({ ...formNewEscale, Nome: e.target.value })}
                />
                <Checkbox
                  id="separar"
                  onCheckedChange={(e) => setFormNewEscale({ ...formNewEscale, SepararGenero: Boolean(e) })}
                  className="m-1"
                />
                <Label htmlFor="separar" className="m-1">Separar Generos</Label>
              </div>
              
              <div className="flex justify-center gap-10">
                <Label htmlFor="Mes escala">Mês da escala</Label>
                <Input
                  id="Mes escala"
                  placeholder="12"
                  className="max-w-[100px] mb-5"
                  onChange={(e) => setFormNewEscale({ ...formNewEscale, Mes: Number(e.target.value) })}
                  required
                />
                <Label htmlFor="Ano escala">Ano da escala</Label>
                <Input
                  id="Ano escala"
                  placeholder="2025"
                  className="max-w-[100px]"
                  onChange={(e) => setFormNewEscale({ ...formNewEscale, Ano: Number(e.target.value) })}
                  required
                />
              </div>
                
              <div className="flex justify-center gap-10">
                <div className="flex-col justify-center">
                  <Label htmlFor="Mes escala">Domingo</Label>
                  <Input
                    id="Mes escala"
                    placeholder="0"
                    className="max-w-[80px]"
                    onChange={(e) => setFormNewEscale({ ...formNewEscale, Domingo: Number(e.target.value) })}
                    required
                  />
                </div>

                <div className="flex-col justify-center">
                  <Label htmlFor="Mes escala">Segunda-feira</Label>
                  <Input
                    id="Mes escala"
                    placeholder="0"
                    className="max-w-[80px]"
                    onChange={(e) => setFormNewEscale({ ...formNewEscale, Segunda: Number(e.target.value) })}
                    required
                  />
                </div>

                <div className="flex-col justify-center">
                  <Label htmlFor="Mes escala">Terça-feira</Label>
                  <Input
                    id="Mes escala"
                    placeholder="0"
                    className="max-w-[80px]"
                    onChange={(e) => setFormNewEscale({ ...formNewEscale, Terca: Number(e.target.value) })}
                    required
                  />
                </div>

                <div className="flex-col justify-center">
                  <Label htmlFor="Mes escala">Quarta-feira</Label>
                  <Input
                    id="Mes escala"
                    placeholder="0"
                    className="max-w-[80px]"
                    onChange={(e) => setFormNewEscale({ ...formNewEscale, Quarta: Number(e.target.value) })}
                    required
                  />
                </div>

                <div className="flex-col justify-center">
                  <Label htmlFor="Mes escala">Quinta-feira</Label>
                  <Input
                    id="Mes escala"
                    placeholder="0"
                    className="max-w-[80px]"
                    onChange={(e) => setFormNewEscale({ ...formNewEscale, Quinta: Number(e.target.value) })}
                    required
                  />
                </div>

                <div className="flex-col justify-center">
                  <Label htmlFor="Mes escala">Sexta-feira</Label>
                  <Input
                    id="Mes escala"
                    placeholder="0"
                    className="max-w-[80px]"
                    onChange={(e) => setFormNewEscale({ ...formNewEscale, Sexta: Number(e.target.value) })}
                    required
                  />
                </div>

                <div className="flex-col justify-center">
                  <Label htmlFor="Mes escala">Sábado</Label>
                  <Input
                    id="Mes escala"
                    placeholder="0"
                    className="max-w-[80px]"
                    onChange={(e) => setFormNewEscale({ ...formNewEscale, Sabado: Number(e.target.value) })}
                    required
                  />
                </div>

              </div>

              <div className="flex justify-center mt-10 gap-10">
                <button 
                  className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-full shadow-md transition"
                  onClick={() => {gerar_escala()}}  
                >
                  Gerar escala
                </button>
              </div>
            </div>
          </CardContent>
        </Card>

      </div>
    </div>
  );
};

export default Index;
