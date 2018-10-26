# -*- coding: utf-8 -*-
import os
from logging import getLogger

from pytz import timezone
from dateutil import parser

from flask import request, render_template, jsonify, current_app, url_for
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const

logger = getLogger(__name__)


class CameraHeatmapPage(MethodView):
    NAME = 'camera-heatmap-page'

    def get(self):
        logger.info('CameraHeatmapPage#get')
        template = current_app.config[const.CAMERA_HEATMAP_TEMPLATE]

        bearer = os.environ.get(const.BEARER_AUTH, '')
        prefix = os.environ.get(const.PREFIX, '')

        if const.PREFIX in os.environ:
            positions_path = os.path.join('/',
                                          os.environ.get(const.PREFIX, '').strip(),
                                          *url_for(CameraHeatmapAPI.NAME).split(os.sep)[1:])
        else:
            positions_path = url_for(CameraHeatmapAPI.NAME)

        return render_template(template, bearer=bearer, path=positions_path, prefix=prefix)


class CameraHeatmapAPI(MethodView):
    NAME = 'camera-heatmap-api'

    def get(self):
        logger.info(f'CameraHeatmapAPI#get')
        st = request.args.get('st')
        et = request.args.get('et')

        tz = current_app.config['TIMEZONE']

        logger.info(f'RobotPositionAPI, st={st} et={et}')
        if not st or not et:
            raise BadRequest({'message': 'empty query parameter "st" and/or "et"'})

        try:
            start_dt = parser.parse(st).astimezone(timezone(tz))
            end_dt = parser.parse(et).astimezone(timezone(tz))
        except (TypeError, ValueError):
            raise BadRequest({'message': 'invalid query parameter "st" and/or "et"'})

        logger.info(f'start_dt={start_dt}, end_dt={end_dt}')

        return jsonify({})
