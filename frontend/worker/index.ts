import { BackgroundSyncPlugin } from 'workbox-background-sync';
import { registerRoute } from 'workbox-routing';
import { NetworkOnly } from 'workbox-strategies';

// Background sync for incident creation
// This allows staff to report incidents even if the stadium Wi-Fi drops.
// When connectivity returns, the browser will automatically retry the request in the background.

const bgSyncPlugin = new BackgroundSyncPlugin('incident-queue', {
  maxRetentionTime: 24 * 60, // Retry for max of 24 Hours (specified in minutes)
});

registerRoute(
  /\/api\/v1\/incidents/i,
  new NetworkOnly({
    plugins: [bgSyncPlugin],
  }),
  'POST'
);

// Listen to push events for offline notifications
self.addEventListener('push', (event: any) => {
  const data = JSON.parse(event?.data.text() || '{}');
  event?.waitUntil(
    (self as any).registration.showNotification(data.title, {
      body: data.message,
      icon: '/icon-192x192.png',
    })
  );
});
