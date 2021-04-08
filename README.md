# Vocabulary Keeper

## Build Status

[![CircleCI](https://circleci.com/gh/infantiablue/voca.svg?style=svg)](https://circleci.com/gh/infantiablue/voca) [![Build Status](https://travis-ci.com/infantiablue/voca.svg?branch=main)](https://travis-ci.com/infantiablue/voca) [![codecov.io](https://codecov.io/github/infantiablue/voca/coverage.svg?branch=main)](https://codecov.io/github/infantiablue/voca?branch=main) 

## Video Demo

[https://youtu.be/SNaoEnfT36E](https://youtu.be/SNaoEnfT36E)

## Live Demo

[https://voca.techika.com](https://voca.techika.com)

## Description

As a non-English speaker, I need to learn new vocabulary consecutively. Before CS50, I usually use Apple Notes to save and review new words. However, it's not really an intuitive way to build a vocabulary base. Then, I tried to find some mobile apps for this purpose, yet almost all the app I found is focused on a flashcard base, which means provide users new and random words to memorize. It's not really what I want for my personal purpose. And with the knowledge (and excitement) from the CS50 class, I decided to build a web app for myself to keep new words I found from daily reading or watching activities.

The goal of the app is to support the user save and memorize new words better and more conveniently. There are features for users as below:

- Lookup a word from Oxford dictionary then save it to their own database
- Browse all the words to review (sorted by time added or alphabet order)
- Search for a saved word
- Add personal notes/images for saved words to have better memorization. (This technique is widely use to improve memory by visualizing things)
- Change password.
- There is a nice dashboard with random word, **quote** and **Today I learned** feed which are feteched from Reddit by using API.

I think that I achieved valuable knowledge by using various kinds of tools, libraries and services to build the project:

- Flask with SQLAchmemy, Flask-Login and Flask-WTF
- PostgreSQL for production database
- SQLite for testing database
- Tailwind CSS framework, PostCSS, jQuery. This is a subtle building process which automatically minify CSS files, build JS files from source then output to `dist` folder
- Make it open source at [GitHub](https://github.com/infantiablue/voca)
- Deployed with gunicorn as WSGI implementation, supervisor for process management and nginx as reversed proxy server
- PyTest (with test coverage is more than 80% and I am still improving)
- This is one of my exciting part of the development stage, I have succesfully configure the app for Continuous Integration with [CircleCI](https://circleci.com) and [TravisCI](https://www.travis-ci.com/)

In the end, I've figured out a good work flow to use a CI/CD service to build and deploy the project.
