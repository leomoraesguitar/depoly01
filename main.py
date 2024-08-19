
import flet as ft

class Resize:
    def __init__(self,page):
        self.page = page
        self.page.on_resize = self.page_resize
        self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
        self.page.overlay.append(self.pw)   

    def page_resize(self, e):
        self.pw.value = f"{self.page.window.width}*{self.page.window.height} px"
        self.pw.update()


class SaveSelectFile2(ft.Row):
    def __init__(self, tipo, nome = None):
        '''
        tipo  == path: seleciona uma pasta (retorna o caminho completo da pasta selecionada)
        tipo  == file: seleciona um arquivo (retorna o caminho completo do arquivo selecionado)
        tipo  == save: sala um arquivo (retorna o caminho completo do arquivo, junto com seu nome)
        
        '''
        super().__init__()
        self.nome = nome
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.tamanho_texto = 500
        self.selected_files = ft.Text(width=self.tamanho_texto, selectable=True, max_lines = 1)
        self._value = self.selected_files.value
        self.tipo = tipo
        self.visible = True

        async def Selecionar_arquivo(_):
            await self.pick_files_dialog.pick_files_async(allow_multiple=True)

        async def Selecionar_pasta(_):
            await self.pick_files_dialog.get_directory_path_async(dialog_title = 'askdjahs', initial_directory = r'D:\baixados\programas_python\TabelaMandado\baixaryoutube\baixar_do_youtube\build\web')

        async def Save1(_):
            await self.pick_files_dialog.save_file_async()            



        if tipo == 'file':
            if self.nome == None:
                self.nome = 'Selecione o arquivo'            
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=Selecionar_arquivo,
                ),
                self.selected_files,
            ]
        elif tipo == 'path':
            if self.nome == None:
                self.nome = 'Selecione a pasta'
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.FOLDER,
                    on_click=Selecionar_pasta,
                ),
                self.selected_files,
            ]   
        elif tipo == 'save':
            if self.nome == None:
                self.nome = 'Digite o nome do arquivo'            
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.SAVE,
                    on_click=Save1,
                ),
                self.selected_files,

            ]                      

    async def pick_files_result(self, e: ft.FilePickerResultEvent):
        if self.tipo == 'file':
            self.selected_files.value = (
                ",".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
            )
        elif self.tipo == 'path':
            self.selected_files.value = e.path if e.path else "Cancelled!"

        elif self.tipo == 'save':
            self.selected_files.value = e.path if e.path else "Cancelled!"            
            

        await self.selected_files.update_async()
        self._value = self.selected_files.value


    # happens when example is added to the page (when user chooses the FilePicker control from the grid)
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()

    # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    def will_unmount(self):
        self.page.overlay.remove(self.pick_files_dialog)
        self.page.update()

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, valor):
        self._value = valor
        self.selected_files.value = valor
        # self.selected_files.update()


class Slider_quad(ft.Container):
    def __init__(self, 
                 min = 0,
                 max = 100,
                 value = 0,
                 width = 200,
                 height = 20,
                 data = None,
                 on_change = None,
                 tooltip = None,
                 bgcolor = None,
                 border_color = None,
                 col = None

        ):
        super().__init__()
        self.height = height
        self.width = width
        self.scale = 0.8
        self._value = value
        self.min = min
        self.max = max
        self.maxx = self.width-40
        self.data = data
        self.on_change = on_change
        self.tooltip = tooltip
        self.bgcolor = bgcolor
        self.col = col
        
        self.border_color = border_color
        if self.border_color is None:
            self.border_color  = 'white,0.5'

        self.border = ft.border.only(ft.BorderSide(0.3,self.border_color),ft.BorderSide(0.3,self.border_color),ft.BorderSide(1,self.border_color),ft.BorderSide(1,self.border_color))
        # self.gesto = Gestos('caixa', movimento_vertical=False, width=self.width-190, func=self.Arrastou)
        # self.gesto.Add_control('campo',ft.Container(content = ft.Text(value = self.gesto.value),bgcolor='white,0.15', width=50, height=self.height,border= self.border))


        self.gesto = ft.Stack()
        self.gesto.controls = [
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    on_vertical_drag_update=self.on_pan_update,  
                    left = round(self.map_value(self._value, in_min=self.min, in_max=self.max, out_min=0, out_max=self.maxx),2), 
                    top = 0,                           
                    content= ft.Container(content = ft.Text(value = self._value, text_align='center', weight = 'BOLD'),bgcolor='white,0.15', width=40, height=self.height,border= self.border),
                    data = self.data,
                    on_double_tap = self.SetarValor
                )            
        ]
          
        self.content = self.gesto
        

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if isinstance(value, int) or isinstance(value, float):
            valor = round(float(value),2)
            if valor >= self.max:
                novo_valor = self.maxx
                novo_texto = self.max
            elif valor <= self.min:
                novo_valor = 0
                novo_texto = self.min
            else:
                y = self.map_value(valor, in_min=self.min, in_max=self.max, out_min=0, out_max=self.maxx)
                novo_valor = round(y,2)
                novo_texto = valor
            self.gesto.controls[0].left = novo_valor
            self.gesto.controls[0].content.content.value = novo_texto
            self.Atualizar()                
            
 

    def Atualizar(self):
        try:
            self.update()
        except:
            pass
    def map_value(self, x, in_min=0, in_max=300, out_min=5, out_max=120):
        return out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min)
    def on_pan_update(self, e: ft.DragUpdateEvent):
        # if self.movimento_vertical:
        #     e.control.top = max(0, e.control.top + e.delta_y)
        # print('casa')
        e.control.left = max(0, e.control.left + e.delta_x)
        
        if e.control.left >= self.maxx:
            e.control.left = self.maxx
        if self.height and e.control.top >= self.height:
            e.control.top = self.height -100 
        # print(e.control.left)     
        # self._value = (e.control.left, e.control.top)
        
        x = e.control.left
        y = self.map_value(x, in_min=0, in_max=self.maxx, out_min=self.min, out_max=self.max)
        novo_valor = round(y,2)
        e.control.content.content.value = novo_valor
        # e.control.update()
        self._value = novo_valor

        if not self.on_change is None:
            self.on_change(e)
        self.Atualizar()
    def Voltar(self,e):
            valor = round(float(e.control.value),2)
            if valor >= self.max:
                novo_valor = self.maxx
                novo_texto = self.max
            elif valor <= self.min:
                novo_valor = 0
                novo_texto = self.min
            else:
                y = self.map_value(valor, in_min=self.min, in_max=self.max, out_min=0, out_max=self.maxx)
                novo_valor = round(y,2)
                novo_texto = valor

            self.gesto.controls[0].left = novo_valor
            self.gesto.controls[0].content.content = ft.Text(value = novo_texto, text_align='center', weight = 'BOLD')
            self._value = valor
            self.Atualizar()

    def SetarValor(self, e):        
        e.control.content.content = ft.TextField(dense = True,  text_size = 9, border=None,border_width = 0,expand=True,  on_submit= self.Voltar)
        self.Atualizar()

class Example(ft.Row):
    def __init__(self):
        super().__init__()
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.selected_files = ft.Text()
    
        async def pick_files(_):
            await self.pick_files_dialog.pick_files_async(allow_multiple=True)
    
        self.controls = [
            ft.ElevatedButton(
                "Pick files",
                icon=ft.icons.UPLOAD_FILE,
                on_click=pick_files,
            ),
            self.selected_files,
        ]
    
    async def pick_files_result(self, e: ft.FilePickerResultEvent):
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        await self.selected_files.update_async()
    
    # happens when example is added to the page (when user chooses the FilePicker control from the grid)
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
    
    # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    def will_unmount(self):
        self.page.overlay.remove(self.pick_files_dialog)
        self.page.update()

def main(page: ft.Page):
    # Definindo o t�tulo da p�gina
    page.title = 'Título'
    page.window.width = 800  # Define a largura da janela como 800 pixels
    page.window.height = 385  # 
    page.theme_mode = ft.ThemeMode.DARK

    Resize(page)
    p = Slider_quad()
    tab = SaveSelectFile2('save')
    s = Example()
        
    page.add(p,tab,ft.Text('meu ovo'),s )

if __name__ == '__main__': 
    # saida = Saida()
    # print = saida.pprint 
    ft.app(target=main)
