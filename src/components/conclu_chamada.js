const template = document.createElement('template');
template.innerHTML = `
    <style>
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box
        }

        div{
            border:solid 5px #A8A7A7;
            border-radius: 20px;
            background-color: #fcfcfc;
            width: 1010px;
            height: 650px;
            font-family:'Poppins', sans-serif;
            display : flex;
            align-items : center;
            flex-direction: column;
        }

        textarea{
            font-family:'Poppins', sans-serif;
            font-size: 18px;
            font-weight:600;
            color: rgba(0,0,0,25%);
            border: solid 2px #A8A7A7;
            border-radius: 10px;
            padding: 10px;
            height: 164px;
            width: 790px;
            resize: vertical;
        }

        button{
            border:none;
            font-size:24px;
            color:#FCFCFC;
            background-color: #57DA74;
            border-radius:10px;
            height: 60px;
            width: 300px;
            margin:40px 0px 56px 0px;
        }

        .chamado{
            font-size:14px;
            align-items: start;
            border: solid 2px #A8A7A7;
            border-radius: 10px;
            padding: 10px;
            height: 200px;
            width: 790px;
            margin-bottom: 30px;
        }
        p{
            padding: 10px 0px;
        }

    </style>
    
    <div>
        <p style="font-size: 36px; padding: 30px 0px 20px 0px; ">
        Conclusão de Chamada</p>  
        <div class="chamado">
            <span><b>TITULO DO CHAMADO xxxxxxxxxxxxxxxX</b>
            <b>11/11/2011</b></span>
            <p><b>Tipo:</b> Problema de Hardware</p>
            <p><b>Descrição:</b> Descrição: é simplesmente uma simulação de texto da indústria tipográfica e de impressos, e vem sendo utilizado desde o século XVI, quando um impressor desconhecido pegou uma bandeja de tipos e os embaralhou para fazer um livro de modelos de tipos. </p>

        </div>
        <textarea name="txtdesc" id="txtdesc">Descreva a conclusão</textarea>
        <button>Concluir chamada</button>
    </div>
       
`;

class Conclusao extends HTMLElement{
    constructor(){
        super();
        console.log('criado');

        this.attachShadow( {mode:'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

    }

    connectedCallback(){
        console.log('callback');
        const button = this.shadowRoot.querySelector('button');
        
    }
}

window.customElements.define('conclu-chamada', Conclusao);