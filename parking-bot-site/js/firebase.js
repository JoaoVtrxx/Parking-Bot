

const config = {
    apiKey: "AIzaSyB7OaNJAUcce0RkYV81AQB6wjdpShBXPso",
    authDomain: "projetointegrador2-abfb0.firebaseapp.com",
    databaseURL: "https://projetointegrador2-abfb0-default-rtdb.firebaseio.com",
    projectId: "projetointegrador2-abfb0",
    storageBucket: "projetointegrador2-abfb0.appspot.com",
    messagingSenderId: "344867624568",
    appId: "1:344867624568:web:ac1ca07ece7fb43be6bf8d",
    measurementId: "G-KQ0Z1YGR0M"
  };

  firebase.initializeApp(config);
 

  var contador = document.getElementById("contador");
  var db = firebaseRef = firebase.database().ref("users");

  db.on('child_added', function(snapchot){
    var adicionado = snapchot.val();

    console.log(adicionado)
    contador.innerHTML = adicionado;
  })


  setInterval(function(){ 
   
    db.on('child_added', function(snapchot){
      var adicionado = snapchot.val();
  
      console.log(adicionado)
      contador.innerHTML = adicionado;
    })

  }, 5000)

  