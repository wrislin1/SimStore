function NewSelection(){
  let x = document.getElementById('medium').value;
  window.alert(x);
}

function isFinished(cb){
  if(cb.checked)
  {
document.getElementById('rating').type="text";
  }

  if(!cb.checked)
  {
document.getElementById('rating').type="hidden";
  }

}




//NewSelection();
