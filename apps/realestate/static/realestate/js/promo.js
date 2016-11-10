$(function() {
  var PromoSlider = new MasterSlider();
  PromoSlider.setup('masterslider-promo' , {
    width: 1400, // PromoSlider standard width
    height: 580, // PromoSlider standard height
    speed: 70,
    layout: 'fullwidth',
    loop: true,
    autoplay: true,
    overPause: true,
    dir: 'v',
    // JJW
    centerControls: true,
    layersMode: "center",
  });
  // Adds Arrows navigation control to the PromoSlider
  PromoSlider.control('arrows');
  PromoSlider.control('lightbox');
  PromoSlider.control('thumblist', {autohide:false, dir:'v', align:'left', width:200, height:120, margin:0, space:10 , hideUnder:500, inset:true});
});
