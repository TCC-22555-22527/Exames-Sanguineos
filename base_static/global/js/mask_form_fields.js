$(document).ready(function($){
    $('#id_cpf').mask('000.000.000-00'); 
    
    var maskBehavior = function (val) {
      return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
    },
    options = {onKeyPress: function(val, e, field, options) {
            field.mask(maskBehavior.apply({}, arguments), options);
        }
    };
    
    $('#id_cell').mask(maskBehavior, options);
});