import os
import uuid
import tempfile
import shutil
from django.core.files import File
from celery import Task
from rodan.models.runjob import RunJob
from rodan.models.runjob import RunJobStatus
from rodan.models.result import Result
from rodan.jobs.gamera import argconvert
from rodan.helpers.thumbnails import create_thumbnails
from gamera.core import init_gamera, load_image  # , save image?
import gamera.toolkits.border_removal

JOB_NAME = 'border_removal.auto_border_removal'


class BorderRemovalAutoTask(Task):
    max_retries = None
    name = JOB_NAME

    def run(self, result_id, runjob_id, *args, **kwargs):
        #Guess what? I'm running.
        runjob = RunJob.objects.get(pk=runjob_id)
        runjob.status = RunJobStatus.RUNNING
        runjob.save()

        #Get appropriate page
        if result_id is None:
            # this is the first job in a run
            page = runjob.page.compat_file_path
        else:
            # we take the page image we want to operate on from the previous result object
            result = Result.objects.get(pk=result_id)
            page = result.result.path

        #Initialize the result
        new_result = Result(run_job=runjob)
        new_result.save()

        result_save_path = new_result.result_path

        #Get the settings. Note that the runtime value is passed inside the 'default' field.
        settings = {}
        for s in runjob.job_settings:
            setting_name = "_".join(s['name'].split(" "))
            setting_value = argconvert.convert_to_arg_type(s['type'], s['default'])
            settings[setting_name] = setting_value

        #Gamera methods begins here
        init_gamera()

        task_image = load_image(page)
        tdir = tempfile.mkdtemp()

        crop_mask = task_image.border_removal(**settings)
        result_image = task_image.mask(crop_mask)
        result_file = "{0}.png".format(str(uuid.uuid4()))
        result_image.save_image(os.path.join(tdir, result_file))

        #Copy over temp file to appropriate result path, and delete temps.
        f = open(os.path.join(tdir, result_file))
        new_result.result.save(os.path.join(result_save_path, result_file), File(f))
        f.close()
        shutil.rmtree(tdir)

        return str(new_result.uuid)

    def on_success(self, retval, task_id, args, kwargs):
        # create thumbnails and set runjob status to HAS_FINISHED after successfully processing an image object.
        result = Result.objects.get(pk=retval)
        result.run_job.status = RunJobStatus.HAS_FINISHED
        result.run_job.save()


        res = create_thumbnails.s(result)
        res.apply_async()

    def on_failure(self, *args, **kwargs):
        runjob = RunJob.objects.get(pk=args[2][1])  # index into args to fetch the failed runjob instance
        runjob.status = RunJobStatus.FAILED
        runjob.save()