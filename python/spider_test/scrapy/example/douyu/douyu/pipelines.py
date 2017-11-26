# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

class ImagesPipeline(ImagesPipeline):
    IMAGE_STORE = get_project_settings().get("IMAGE_STORE")
    print '-'*18
    print IMAGE_STORE
    def get_media_requests(self,item,info):
        image_url = item["imagesUrls"]
        print '*'*18
        print image_url
        yield scrapy.Request(image_url)

    def item_completed(self,results,item,info):
        image_path = [x["path"] for ok,x in result if ok]

        os.rename(self.IMAGE_STORE+"/"+image_path[0],self.IMAGE_STORE+"/"+item["name"]+".jpg")
        item["imagePath"] = self.IMAGE_STORE+"/"+item["name"]

        return item
