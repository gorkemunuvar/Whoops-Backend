from fileinput import filename
from flask import request, send_file
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required, get_jwt_identity

from helpers import image_helper
from helpers.strings import gettext
from schemas import image
from schemas.image import ImageSchema

import os
import traceback


image_schema = ImageSchema()


class ImageUpload(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """
        Used to upload an image file.
        It uses JWT to retrieve user information and then saves the image to the user's folder
        If there is a filename conflict, it appends a number at the end.
        """
        # request.files -> {'image': FileStorage}
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()

        # static/images/user_1
        folder = f"user_{user_id}"

        try:
            image_path = image_helper.save_image(data['image'], folder=folder)
            basename = image_helper.get_basename(image_path)

            return {'message': gettext('image_uploaded').format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data['image'])

            return {'message': gettext('image_illegal_extension').format(extension)}, 400


class Image(Resource):
    @classmethod
    @jwt_required()
    def get(cls, filename: str):
        """
        Returns the requested image if it exist. Looks up inside the logged in user's folder.
        """

        user_id = get_jwt_identity()
        folder = f'user_{user_id}'

        if not image_helper.is_filename_safe(filename):
            return {'message': gettext('image_illegal_file_name').format(filename)}, 400

        try:
            absolute_path = image_helper.get_path(filename, folder=folder)
            return send_file(absolute_path)
        except FileNotFoundError:
            return {'message': gettext('image_not_found').format(filename)}, 404

    @classmethod
    @jwt_required()
    def delete(cls, filename: str):
        user_id = get_jwt_identity()
        folder = f'user_{user_id}'

        if not image_helper.is_filename_safe(filename):
            return {'message': gettext('image_illegal_file_name').format(filename)}, 400

        try:
            absolute_path = image_helper.get_path(filename, folder=folder)
            print(absolute_path)
            os.remove(absolute_path)
            return {'message': gettext('image_deleted').format(filename)}, 200
        except FileNotFoundError:
            return {'message': gettext('image_not_found').format(filename)}, 404
        except:
            traceback.print_exc()
            return {'message': gettext('image_deleted_failed')}, 500


class AvatarUpload(Resource):
    @classmethod
    @jwt_required()
    def put(cls):
        """
        This endpoint is used to upload user avatars. All avatars are named after the user's ID.
        Somethin like this: user_{id}{ext}
        Uploading a new avatar overwrites the existing one.
        """
        data = image_schema.load(request.files)
        filename = f'user_{get_jwt_identity()}'
        folder = 'avatars'
        avatar_path = image_helper.find_image_any_format(filename, folder)

        extension = image_helper.get_extension(data['image'].filename)

        # if the extension is not an image ext. flow should not be allowed to continue.
        # Also uppercase image extensions is not allowed by flask_upload module.
        if not extension[1:] in image_helper.IMAGE_EXTENSIONS:
            return {'message': gettext('image_illegal_extension').format(extension)}, 400

        # if the image exists
        if avatar_path:
            try:
                # delete the image
                os.remove(avatar_path)
            except:
                return {'message': gettext('avatar_delete_failed')}, 500

        try:
            avatar = filename + extension
            avatar_path = image_helper.save_image(
                data['image'], folder=folder, name=avatar
            )
            basename = image_helper.get_basename(avatar_path)

            return {'message': gettext('avatar_uploaded').format(basename)}, 200
        except UploadNotAllowed:
            return {'message': gettext('image_illegal_extension').format(extension)}, 400


class Avatar(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id: int):
        """
        Returns the requested avatar if it exist. Looks up inside the logged in user's folder.
        """
        folder = 'avatars'
        filename = f'user_{user_id}'
        avatar = image_helper.find_image_any_format(filename, folder)

        # if the avatar exists
        if avatar:
            return send_file(avatar)

        return {'message': gettext('avatar_not_found')}, 404
