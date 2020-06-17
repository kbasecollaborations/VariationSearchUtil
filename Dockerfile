FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN touch new
RUN curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs
RUN npm install --save @gmod/tabix @gmod/vcf 
RUN pip install --upgrade pip && \
    pip install pandas==0.24.1 && \
    pip install --upgrade --extra-index-url https://pypi.anaconda.org/kbase/simple \
      kbase-workspace-client==0.3.0


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
