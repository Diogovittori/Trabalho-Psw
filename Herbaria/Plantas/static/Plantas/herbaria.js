/* Integração dos plugins locais do Alazea com as páginas Django. */
(function ($) {
    'use strict';
    $(function () {
        if ($.fn.magnificPopup) {
            $('.herbaria-gallery').each(function () {
                $(this).magnificPopup({
                    delegate: 'a.portfolio-img',
                    type: 'image',
                    gallery: {enabled: true, tPrev: 'Anterior', tNext: 'Próxima', tCounter: '%curr% de %total%'},
                    tClose: 'Fechar (Esc)',
                    tLoading: 'Carregando…',
                    image: {tError: 'Não foi possível carregar a imagem.', titleSrc: function (item) {
                        // Usar texto escapado: nomes de plantas são dados do usuário.
                        return $('<span>').text(item.el.find('img').attr('alt') || '').html();
                    }}
                });
            });
        }
        // Bootstrap já controla o menu responsivo por data-toggle="collapse".
        // Não inicializar ClassyNav sobre o mesmo menu.
        // A pesquisa agora ? enviada por GET e executada no banco pelo Django.
    });
})(jQuery);
