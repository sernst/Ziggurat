#!/bin/bash

gunicorn -b localhost:8000 application.py
