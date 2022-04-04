
const template = document.createElement('template');
template.innerHTML = `  
    <style>
    * {
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        font-family: Poppins, sans-serif;
    }

    :root {

        /*CORES*/
        --principal-background: #FCFCFC;
        --navbar-color:#B8D7D9;
    
        --card-color:#A8A7A7;
    
        --text-principal-color: #000000;
        --text-navbar-color:#6D6D6D;
        
         /*FONTES*/
        --font-semibold: 600;
        --font-medium: 500;
        --font-regular: 400 ;
    }
    
    
    form {
        border:solid  3px #A8A7A7; 
        border-radius: 15px;
        padding: 48px 36px;
    
        margin: 10%  20%;
    
        background-color: #FCFCFC;   
    }
    
    label{
        margin-bottom: 8px; 
        font-weight: 500;
    }
    
    .title {
        display: flex;
        justify-content: space-between;
        margin-bottom: 24px;
    }
    
    .title input {
        width: 100%;
    }
    
    
    .title input, .title select{
        display: block;
        border:solid  2px #A8A7A7;
        border-radius: 10px;
        height: 35px;
        padding: 0px 10px;
    }
    
    select {
        border:solid  2px #A8A7A7;
        border-radius: 10px;
        height: 35px;
        width: 100%;
    }
    
    .description textarea{
        border:solid  2px #A8A7A7;
        border-radius: 10px;
        padding: 5px 10px;
        height: 140px;
        width: 100%;
        margin-bottom: 24px;
        resize:vertical;   
    }
    
    .archive input{
        border:solid  2px #A8A7A7;
        border-radius: 10px;
        height: 35px;
        width: 260px;
    }
    
    
    
    .buttons{
        display: flex;
        justify-content: center;
        margin: 40px 0px 0px 0px;
    }
    
    .enviar{
        background-color: rgba(87, 218, 116, 70%);
        border-radius: 15px;
        font-weight: 500;
        height: 50px;
        width: 200px;
        border:none;
    }
    
    .limpar{
        background-color: rgba(255, 224, 66, 90%);
        border-radius: 15px;
        font-weight: 500;
        height: 50px;
        width: 200px;
        border:none;
        margin-right: 56px;
    }
    

    </style>

    <form action="/" method="post">
                <div class="title">
                    <div>
                        <label>Titulo</label>
                        <input type="text" id="title" name="title">
                    </div>
                    <div>
                        <label>Tipo</label>
                        <select>
                            <option>Problemas de Software</option>
                            <option>Problemas de Hardware</option>
                            <option>Dúvidas ou Esclarecimentos</option>
                        </select>
                    </div> 
                </div> 
                <div class="description">
                    <label>Descrição</label> <br>
                    <textarea id="description" name="description"></textarea> 
                </div>
                <div class="archive">
                    <label>Anexar arquivo (PNG, JPEG, JPG)</label> <br>
                    <input type="file" id="archive" name="archive"> 
                </div> 

                <div class="buttons">
                    <input class="limpar" type="button" value="Limpar">
                    <input class="enviar" type="button" value="Enviar">                   
                </div>
            </form>
    
`;
    
class formulario extends HTMLElement {
    constructor(){
        super();

        this.attachShadow({mode:'open'})
        this.shadowRoot.appendChild(template.content.cloneNode(true))
    }  
}

window.customElements.define('requisition-form', formulario);