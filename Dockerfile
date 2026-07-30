FROM odoo:19

USER root

RUN apt-get update && \
    apt-get install -y \
        git \
        nano \
        vim \
        curl \
        wget \
        unzip \
        build-essential \
        python3-dev \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install common Python packages
RUN pip3 install --no-cache-dir \
    pandas \
    openpyxl \
    xlrd \
    xlsxwriter \
    pillow \
    requests \
    python-dateutil \
    psycopg2-binary

RUN mkdir -p \
    /mnt/extra-addons \
    /etc/odoo \
    /var/lib/odoo \
    /var/log/odoo

RUN chown -R odoo:odoo \
    /mnt/extra-addons \
    /etc/odoo \
    /var/lib/odoo \
    /var/log/odoo

USER odoo

EXPOSE 8069

CMD ["odoo"]