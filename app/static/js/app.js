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
            
            <li class="nav-item active">
              <router-link class="nav-link" to="/register">Register</router-link>
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

//registration
const Register=Vue.component("register",{
  
    
  template:`
        <div class = everything>
          
          <h3 class="card-header center text-muted">Register</h3>
          <div class="card center">
           
            <form id="register" @submit.prevent="Register" enctype="multipart/form-data">
            <div>
                <label>Firstname:</label><br/>
                
               <input type='text' id='firstname' name='firstname' style="width: 100%;"/>
            </div>
            <div>
                <label>Lastname:</label><br/>
               <input type='text' id='lastname' name='lastname' style="width: 100%;"/>
            </div>
            <div>
                <label>Username:</label><br/>
               <input type='text' id='username' name='username' style="width: 100%;"/>
               
            </div>
            <div>
                <label>Password:</label><br/>
               <input type='password' id='password' name='password' style="width: 100%;"/>
            </div>
            <div>
                <label>Email:</label><br/>
               <input type='text' id='email' name='email' placeholder="jdoe@example.com" style="width: 100%;"/>
            </div>
            <div>
                <label>Location:</label><br/>
               <input type='text' id='location' name='location' style="width: 100%;"/>
            </div>
            <div>
                <label>Biography:</label><br/>
               <textarea name="biography" rows="3" style="width:100%"> </textarea><br/>
            </div>
            <div>
                <label for='photo' class='btn btn-primary'>Browse....</label> <span>{{ filename }}</span>
                
                <input id="photo" type="file" name='photo' style="display: none" v-on:change = "onFileSelected" /><br/>
                
            </div>
                <br/>
                 <div>
                      <input type="submit" id="submit" class="btn btn-success" value="Register" /> 
                    </div>
                
            </form>
            <div v-if='messageFlag' style="margin-top: 5%;">
            
                <div v-if="!errorFlag ">
                    <div class="alert alert-success" >
                        {{ message }}
                    </div>
                </div>
                <div v-else >
                    <ul class="alert alert-danger">
                        <li v-for="error in message">
                            {{ error }}
                        </li>
                    </ul>
                </div>
                
            </div>
        </div>
    </div>
  `,
   methods: {
      Register : function(){
          let self = this;
          let register = document.getElementById('register');
          let form_data = new FormData(register);
          
          fetch("/api/users/register", {
              method: "POST",
              body: form_data,
              headers: {
              'X-CSRFToken': token
              },
              credentials: 'same-origin'
          }).then(function(response){
              return response.json();
          }).then(function (jsonResponse) {
              // display a success message
              self.messageFlag = true
              
              if (jsonResponse.hasOwnProperty("errors")){
                  self.errorFlag=true;
                  self.message = jsonResponse.errors;
              }else if(jsonResponse.hasOwnProperty("message")){
                  router.push("/login");
              }
        });
      },
      onFileSelected: function(){
        let self = this
        let filenameArr = $("#photo")[0].value.split("\\");
        self.filename = filenameArr[filenameArr.length-1]
      }
   },
   data: function(){
     return {
        errorFlag: false,
        messageFlag: false,
        message: [],
        filename: "No File Selected"
    }
   }
});





const Login = Vue.component('login', {
    template:`
     <div>
        <form id="login-form" @submit.prevent="login">
            <div class="card-header center">
              <strong>Login</strong>
            </div>
            <div class="card center">
              <div class="card-body login">
                <div style="margin-top:5%;">
                  <label for='username'><strong>Username</strong></label><br>
                  <input type='text' id='username' name='username' style="width: 100%;"/>
                </div>
                <div style="margin-top:5%;">
                  <label for='password'><strong>Password</strong></label><br>
                  <input type='password' id='password' name='password' style="width: 100%;"/>
                </div>
                <div style="margin-top:5%;">
                  <button id="submit" class="btn btn-success">Login</button> 
                </div>
                <div v-if='messageFlag' style="margin-top:5%;">
                  <div class="alert alert-danger center" style="width: 100%; margin-top: 5%;">
                    {{ message }}
                  </div>
                </div>
              </div>
            </div>
        </form>
      </div>
    `,
    methods:{
      login: function(){
        const self = this
        
        let login_data = document.getElementById('login-form');
        let login_form = new FormData(login_data);
        
        fetch("/api/auth/login",{
          method: "POST",
          body: login_form,
          headers: {
          'X-CSRFToken': token
          },
          credentials: 'same-origin'
        }).then(function(response){
          return response.json();
        }).then(function(jsonResponse){
          self.messageFlag = true;
          
          if(jsonResponse.hasOwnProperty("token")){
            cuser={"token":jsonResponse.token, id: jsonResponse.user_id};
            localStorage.current_user = JSON.stringify(cuser);
            
            router.go();
            router.push("/explore")
          }else{
            self.message = jsonResponse.errors
          }

        }).catch(function(error){
          self.messageFlag = false;
          console.log(error);
        });
      }
    },
    data: function(){
      return {
        messageFlag: false,
        message: ""
      }
    }
    
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
        // {path: "/upload", component: Upload},
        {path: "/register/", component: Register},
        {path: "/login/", component: Login},
        
        
        
        // This is a catch all route in case none of the above matches
        {path: "*", component: NotFound}
    ]
});

// Instantiate our main Vue Instance
let app = new Vue({
    el: "#app",
    router
});