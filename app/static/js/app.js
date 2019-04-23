/* Add your Application JavaScript */
Vue.component('app-header', {
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <img src='static/images/logo.png' class="small-logo"/>
      <a class="navbar-brand" href="/">Photogram</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        </ul>
      </div>
      
        <ul class="navbar-nav">
            <li class="nav-item active">
                <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
            </li>
            <li class="nav-item active">
              <router-link class="nav-link" to="/explore">Explore</router-link>
            </li>
            
            <li class="nav-item active">
              <router-link class="nav-link" :to="{name: 'users', params: {user_id: cu_id}}">My Profile</router-link>
            </li>
            <li v-if="auth" class="nav-item active">
              <router-link class="nav-link" to="/logout">Logout</router-link>
            </li>
            
            <li v-else class="nav-item">
              <router-link class="nav-link active" to="/login">Login</router-link>
            </li>
        </ul>
    </nav>
    `,
    data: function(){
        return {
            auth: localStorage.hasOwnProperty("current_user"),
            cu_id: localStorage.hasOwnProperty("current_user") ? JSON.parse(localStorage.current_user).id : null
        }
    }
});

Vue.component('app-footer', {
    template: `
    <footer>
        <div class="container">
            <p>Copyright &copy; Flask Inc.</p>
        </div>
    </footer>
    `
});

const Home = Vue.component('home', {
   template: `
    <div class="jumbotron">
        <h1>Photogram</h1>

    </div>
   `,
    data: function() {
       return {}
    }
});


const Registration = Vue.component('registration-form',{
    template:`
    <div>
    <h1>Upload Photo</h1>
    
        <form id="registrationForm" @submit.prevent="UploadForm" enctype="multipart/form-data">
            <label>Description:</label><br/>
            <textarea name='description'></textarea><br/>
            <label for='photo' class='btn btn-primary'>Browse....</label> <span>{{ filename }}</span>
            <input id="photo" type="file" name='photo' style="display: none" v-on:change = "onFileSelected" /><br/>
            <input type="submit" value="Upload" class="btn btn-success"/>
        </form>
    </div>
    `,
    methods: {
        UploadForm: function(){
            let self = this;
            let uploadForm = document.getElementById('uploadForm');
            let form_data = new FormData(uploadForm);
            
            fetch("/api/upload", {
                method: "post",
                body: form_data,
                headers: {
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            }).then(function(response){
                return response.json();
            }).then(function (jsonResponse) {
                // display a success message
                self.messageFlag = true;
                if (jsonResponse.hasOwnProperty("errors")){
                    self.errorFlag=true;
                    self.message = jsonResponse.errors;
                }else if(jsonResponse.hasOwnProperty("message")){
                    self.errorFlag = false;
                    self.message = "File Upload Successful";
                    self.cleanForm();
                }
             })
             .catch(function (error) {   
                console.log(error);
             });
        },
        cleanForm : function(){
            let form =$("#uploadForm")[0];
            let self = this;
            
            form.description.value = "";
            form.photo.value = "";
            self.filename = "";
        },
        onFileSelected: function(){
            let self = this;
            let filenameArr = $("#photo")[0].value.split("\\");
            self.filename = filenameArr[filenameArr.length-1];
        }
    },
    data: function(){
        return {
            errorFlag: false,
            messageFlag: false,
            message: [],
            filename: ""
        };
    },
    
});

const NotFound = Vue.component('not-found', {
    template: `
    <div>
        <h1>404 - Not Found</h1>
    </div>
    `,
    data: function () {
        return {};
    }
});

// Define Routes
const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: "/", component: Home},
        {path: "/upload", component: Upload},
        
        
        
        
        // This is a catch all route in case none of the above matches
        {path: "*", component: NotFound}
    ]
});

// Instantiate our main Vue Instance
let app = new Vue({
    el: "#app",
    router
});