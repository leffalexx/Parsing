from scrapy.pipelines.images import ImagesPipeline
import hashlib

class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        image_id = hashlib.shal(request.url.encode()).hexdigest()
        return f"{item['author']} - {image_id}.jpg"