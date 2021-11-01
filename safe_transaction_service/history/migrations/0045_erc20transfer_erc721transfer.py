# Generated by Django 3.2.8 on 2021-10-29 11:13

import django.db.models.deletion
from django.db import migrations, models

import gnosis.eth.django.models


def migrate_data(apps, schema_editor):
    EthereumEvent = apps.get_model("history", "EthereumEvent")
    ERC20Transfer = apps.get_model("history", "ERC20Transfer")
    ERC721Transfer = apps.get_model("history", "ERC721Transfer")

    for event in EthereumEvent.objects.all().iterator():
        parameters = {
            "ethereum_tx_id": event.ethereum_tx_id,
            "log_index": event.log_index,
            "address": event.address,
            "_from": event.arguments["from"],
            "to": event.arguments["to"],
        }
        if "tokenId" in event.arguments:
            parameters["token_id"] = event.arguments["tokenId"]
            ERC721Transfer.objects.create(**parameters)
        elif "value" in event.arguments:
            parameters["value"] = event.arguments["value"]
            ERC20Transfer.objects.create(**parameters)


class Migration(migrations.Migration):

    dependencies = [
        ("history", "0044_reprocess_module_txs"),
    ]

    operations = [
        migrations.CreateModel(
            name="ERC20Transfer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "address",
                    gnosis.eth.django.models.EthereumAddressField(db_index=True),
                ),
                ("_from", gnosis.eth.django.models.EthereumAddressField(db_index=True)),
                ("to", gnosis.eth.django.models.EthereumAddressField(db_index=True)),
                ("log_index", models.PositiveIntegerField()),
                ("value", gnosis.eth.django.models.Uint256Field()),
                (
                    "ethereum_tx",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="history.ethereumtx",
                    ),
                ),
            ],
            options={
                "verbose_name": "ERC20 Transfer",
                "verbose_name_plural": "ERC20 Transfers",
            },
        ),
        migrations.CreateModel(
            name="ERC721Transfer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "address",
                    gnosis.eth.django.models.EthereumAddressField(db_index=True),
                ),
                ("_from", gnosis.eth.django.models.EthereumAddressField(db_index=True)),
                ("to", gnosis.eth.django.models.EthereumAddressField(db_index=True)),
                ("log_index", models.PositiveIntegerField()),
                ("token_id", gnosis.eth.django.models.Uint256Field()),
                (
                    "ethereum_tx",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="history.ethereumtx",
                    ),
                ),
            ],
            options={
                "verbose_name": "ERC721 Transfer",
                "verbose_name_plural": "ERC721 Transfers",
            },
        ),
        migrations.RunPython(migrate_data, reverse_code=migrations.RunPython.noop),
    ]