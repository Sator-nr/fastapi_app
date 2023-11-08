from fastapi import UploadFile, APIRouter
import shutil

from src.tasks.tasks import process_pic

router = APIRouter(
    prefix='/images',
    tags=['Загрузка картинок']
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f'src/static/images/{name}.webp'
    with open(im_path, 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)

