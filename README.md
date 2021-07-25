# Description

This is just a [proxy charm](https://discourse.charmhub.io/t/proxy-charm-request-for-image-registry/3916)
to allow the inclusion of remotely running Thruk agents as peers to the locally
running [thruk-master-k8s](https://charmhub.io/thruk-master-k8s) application.

The remote Thruk agent can be deployed using Juju (for instance using a
[thruk-agent](https://charmhub.io/thruk-agent) application related to a
[Nagios](https://charmhub.io/nagios) one), or be independently deployed. The
only requirement is HTTP connectivity between the locally running Thruk master
unit and the remote Thruk agent.

This charm is the Kubernetes version of the
[thruk-external-agent](https://charmhub.io/thruk-external-agent) charm. Do note
that at the time of writing, [Juju does not yet support proxy charms](https://bugs.launchpad.net/juju/+bug/1826205)
on Kubernetes environments. This means that a workload container is still
required even though it sits idle. It's recommended to use a very lightweight
image such as Alpine as the workload image.

# Usage

As a proxy charm, all it needs is some information about the remote Thruk agent
it stands for plus a name to use in the local Thruk master. In this case these
are required:

- `url`: This is the URL of the remote Thruk agent.
- `thruk_key`: This is the key of the remote Thruk agent.
- `nagios_context`: This will be used as the peer and section names in the
  local Thruk master.

This information is communicated to the Thruk master unit upon establishing the
`thruk-agent` relation to it:

    juju deploy thruk-master-k8s --resource thruk-image=meyer91/thruk
    juju deploy proxy-thruk-agent some-external-site --resource stub-image=alpine \
        --config url=http://url.to.remote.thruk.agent.com/thruk \
        --config thruk_key=fhwjr928 \
        --config nagios_context=some-external-site
    juju relate thruk-master-k8s some-external-site
