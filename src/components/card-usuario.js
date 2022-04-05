
const template = document.createElement('template');
template.innerHTML = `  
    <style type="text/css">
      * {
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
      }

      .card{
          border:solid 2px #A8A7A7;
          border-radius: 10px;
          width:100% ;
          height:70px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0px 16px;
      }

      .titulo {
          font-weight: 600;
      } 

      .problema{
          display: flex;
          align-items: center;
      }

      .mais {
          display: flex;
          align-items: center;
          margin-right: 56px;
      }

      .icon {
          height: 50px;
          width: 50px;   
      }
      </style>

        <div class="card">
          <p class="titulo">aaaaaaa</p><!--variavel titulo-->
          <div class="problema">
              <p class="mais">Ver mais <img src="../static/images/Seta.svg" alt="Seta"> </p>
              <img class="icon" src="../static/images/Hardware.png" alt="icon"> <!--variavel icon-->
          </div>
        </div>
`;
    
class carduser extends HTMLElement {
    constructor(){
        super();

        this.attachShadow({mode:'open'})
        this.shadowRoot.appendChild(template.content.cloneNode(true))
    }  
}

window.customElements.define('card-user', carduser);