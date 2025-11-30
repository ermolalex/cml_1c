from oscar.apps.catalogue.views import ProductCategoryView as CoreProductCategoryView

class ProductCategoryView(CoreProductCategoryView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name)
        context.update(search_context)
        context.update({'test':'test'})
        return context
