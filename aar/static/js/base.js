$(function(){
  $('img.polaroid').wrap('<figure class="polaroidWrap" />');

  $("img.polaroid").each(function(index){
    caption=$(this).data("caption");
    figcaption="<figcaption>"+caption+"</figcaption>";
    $(figcaption).insertAfter($(this));
  });
});