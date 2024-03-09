function swapImg(){

  el = document.getElementById("heart")
  console.log(el)
  if (el.img.src == "{% static 'genioapp/img/heart_filled=false.png' %}") {
    el.firstElementChild.src = "{% static 'genioapp/img/heart_filled=true.png' %}";

    // el.img.src = "{% static 'genioapp/img/heart_filled=true.png' %}"
  } else {
    el.firstElementChild.src = "{% static 'genioapp/img/heart_filled=false.png' %}";

    // el.img.src = "{% static 'genioapp/img/heart_filled=false.png' %}"
  }
}