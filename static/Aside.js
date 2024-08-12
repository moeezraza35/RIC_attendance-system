function show_hide_aside(){
    var Aside = document.querySelector("aside");
    if (Aside.style.display == "block"){
        Aside.style.display = "none";
    }else{
        Aside.style.display = "block";
    };
};